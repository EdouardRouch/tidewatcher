#!/usr/bin/env python3

import os
import time
import requests
import threading
import logging
import watchdog.events
from watchdog.observers.polling import PollingObserver
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Configuration from environment
VERSION = "1.0.0"

jellyfin_api_key_file = os.getenv("JELLYFIN_API_KEY_FILE", "/run/secrets/jellyfin_api_key")
if os.path.isfile(jellyfin_api_key_file):
    with open(jellyfin_api_key_file, "r") as f:
        JELLYFIN_API_KEY = f.read().strip()
else:
    JELLYFIN_API_KEY = os.getenv("JELLYFIN_API_KEY", "")

JELLYFIN_URL = os.getenv("JELLYFIN_URL", "http://127.0.0.1:8096")
MEDIA_FOLDER = os.getenv("MEDIA_FOLDER", "/data")
LOG_TO_FILE = os.getenv("LOG_TO_FILE", "false").lower() == "true"
LOG_TO_STDOUT = os.getenv("LOG_TO_STDOUT", "true").lower() == "true"
LOGFILE = os.getenv("LOGFILE", "/var/log/tidewatcher.log")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
DELAY_SECONDS = int(os.getenv("DELAY_SECONDS", 60))
POLL_TIMEOUT = int(os.getenv("POLL_TIMEOUT", 5))
DATE_FORMAT = os.getenv("DATE_FORMAT", "%Y-%m-%d %H:%M:%S")

default_filetypes = [
    "*.mkv", "*.mp4", "*.avi", "*.m4v", "*.mov", "*.ts", "*.vob", "*.webm",
    "*.mp3", "*.mp2", "*.ogg", "*.flac", "*.m4a", "*.srt", "*.sub",
    "*.ass", "*.idx", "*.smi"
]
filetypes = os.getenv("FILETYPES", "")
FILETYPES = filetypes.split(",") if filetypes else default_filetypes

ignored_files = os.getenv("IGNORED_FILES","")
IGNORED_FILES = ignored_files.split(",") if ignored_files else []

# State control
refresh_timer: threading.Timer = None
lock = threading.Lock()

# Setup logging
def setup_logger():
    """
    Configures and returns a logger for the 'tidewatcher' application.

    The logger is set up with the log level specified by the global LOG_LEVEL variable.
    Log messages are formatted using the global DATE_FORMAT variable.
    Depending on the global flags LOG_TO_STDOUT and LOG_TO_FILE, log messages are sent to stdout and/or a file specified by LOGFILE.

    Returns:
        logging.Logger: Configured logger instance for 'tidewatcher'.
    """
    logger = logging.getLogger("tidewatcher")
    logger.setLevel(getattr(logging, LOG_LEVEL))
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt=DATE_FORMAT)

    if LOG_TO_STDOUT:
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    if LOG_TO_FILE:
        fh = logging.FileHandler(LOGFILE)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger

logger = setup_logger()

def get_headers():
    """
    Generate HTTP headers required for authenticating requests to the Jellyfin API.

    Returns:
        dict: A dictionary containing the 'Authorization' header with the Jellyfin API token and client information.
    """
    return {"Authorization": f'MediaBrowser Token="{JELLYFIN_API_KEY}", Client="tidewatcher {VERSION}"'}

def is_scan_running():
    """
    Checks if the "Scan Media Library" scheduled task is currently running on the Jellyfin server.

    Returns:
        bool: True if the "Scan Media Library" task is running, False otherwise.
    """
    response = requests.get(f"{JELLYFIN_URL}/ScheduledTasks", headers=get_headers(), timeout=10)
    if response.status_code == 200:
        for task in response.json():
            if task.get("Name") == "Scan Media Library" and task.get("State") == "Running":
                return True
    return False

def send_refresh_request():
    """
    Sends a refresh request to the Jellyfin server, if no scan is currently running.

    Globals:
        refresh_timer: Resets the refresh timer to None within a thread-safe lock.

    Exceptions:
        Logs any exceptions encountered during the API request.

    Returns:
        None
    """
    global refresh_timer
    
    logger.debug("Library refresh request starting")

    with lock:
        refresh_timer = None
    
    try:
        if is_scan_running():
            queue_refresh("Library refresh already in progress")
            return

        response = requests.post(f"{JELLYFIN_URL}/Library/Refresh", headers=get_headers(), timeout=10)

        if response.status_code == 204:
            logger.info("Library refresh triggered successfully.")
        else:
            logger.error(f"Failed to refresh: {response.status_code} {response.text}")
    except Exception as e:
        logger.error(f"Jellyfin API connection failed: {e}")

def queue_refresh(event:str):
    def queue_refresh(event: str):
        """
        Schedules a refresh request to be sent after a predefined delay.

        If a refresh is already scheduled and pending, logs the remaining time and does not reschedule.
        Otherwise, starts a new timer to send the refresh request after DELAY_SECONDS.

        Args:
            event (str): The name or description of the event triggering the refresh.

        Logs:
            - Debug message if a refresh is already scheduled.
            - Info message with the scheduled refresh time.
        """
    global refresh_timer

    with lock:
        if refresh_timer and refresh_timer.is_alive():
            remaining = int(refresh_timer.interval - (time.time() - refresh_timer.start_time))
            logger.debug(f"Refresh already scheduled in {remaining} seconds")
            return
        next_time = time.time() + DELAY_SECONDS
        refresh_timer = threading.Timer(DELAY_SECONDS, send_refresh_request)
        refresh_timer.start_time = time.time()
        refresh_timer.start()
    logger.info(f"{event} Refresh scheduled at {datetime.fromtimestamp(next_time).strftime(DATE_FORMAT)}")

class Handler(watchdog.events.PatternMatchingEventHandler):
    """
    Handler class for monitoring file system events using watchdog.

    This class extends PatternMatchingEventHandler to handle specific file events
    such as creation, deletion, and movement of files matching specified patterns.

    Methods:
        __init__(): Initializes the handler with file type patterns and ignored files.
        on_created(event): Handles file creation events and triggers a refresh.
        on_deleted(event): Handles file deletion events and triggers a refresh.
        on_moved(event): Handles file movement events and triggers a refresh.
    """
    def __init__(self):
        super().__init__(patterns=FILETYPES, ignore_patterns=IGNORED_FILES,
                         ignore_directories=False, case_sensitive=False)

    def on_created(self, event):
        queue_refresh(f"File created: {event.src_path}")

    def on_deleted(self, event):
        queue_refresh(f"File removed: {event.src_path}")

    def on_moved(self, event):
        queue_refresh(f"File moved: {event.src_path} → {event.dest_path}")

def main():
    """
    Main entry point of the program.
    Starts the observer and monitors changes in the media folder.
    """
    logger.info(f"tidewatcher {VERSION} started. Watching {MEDIA_FOLDER}")
    observer = PollingObserver(timeout=POLL_TIMEOUT)
    observer.schedule(Handler(), path=MEDIA_FOLDER, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()

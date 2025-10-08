# tidewatcher

A Jellyfin media library refresher that watches for filesystem changes and triggers library scans automatically.

> **Note:** This project is a fork of [`giuseppe99barchetta/watchertoucher`](https://github.com/giuseppe99barchetta/watchertoucher).  
> Enhancements include :
> - expanded configuration via environment variables
> - support for Docker secrets for the Jellyfin API key
> - a reformatted and simplified multithreading implementation
> - a reworked logging system

## Features

- Watches your media library folder for new, deleted, or moved media files.
- Debounces multiple file changes and triggers Jellyfin library refresh with a configurable delay.
- Supports a variety of media file types and subtitle formats.
- Configurable via environment variables or `.env` file.
- Logs events to stdout and/or a log file.
- Dockerized for easy deployment.
- Support for docker secrets for sensitive data.
- Uses polling observer for better compatibility with network filesystems.


## Usage

### Requirements

- Python 3.11+
- `watchdog`, `requests`, `python-dotenv` Python packages (installed via `pip install -r requirements.txt`)
- Jellyfin server with an API key

### Environment Variables

Configure your settings via a `.env` file or environment variables:

| Variable            | Description                                                             | Default                           |
|---------------------|-------------------------------------------------------------------------|-----------------------------------|
| JELLYFIN_URL        | Jellyfin server URL                                                     | `http://127.0.0.1:8096`           |
| JELLYFIN_API_KEY    | Jellyfin API token                                                      | `""`                              |
| JELLYIN_API_KEY_FILE| Path to the file containing Jellyfin API token (docker secrets)         | `/run/secrets/jellyfin_api_key`   |
| MEDIA_FOLDER        | Absolute path to your media library                                     | `/data`                           |
| LOG_TO_FILE         | Enable logging to file (`true` or `false`)                              | `false`                           |
| LOG_TO_STDOUT       | Enable logging to stdout (`true` or `false`)                            | `true`                            |
| LOGFILE             | Path to the log file (for `LOG_TO_FILE=true`)                           | `/var/log/tidewatcher.log`        |
| LOG_LEVEL           | Minimum log level to report (e.g `DEBUG`, `INFO`, `ERROR`, `CRITICAL`)  | `INFO`                            |
| DATE_FORMAT         | Date format to use for logs                                             | `%d-%m-%Y %H:%M:%S`               |
| DELAY_SECONDS       | Delay before triggering refresh (to debounce)                           | `60`                              |
| POLL_TIMEOUT        | Polling observer timeout (seconds)                                      | `5`                               |
| FILETYPES           | Comma separated list of file patterns to watch for events               | `*.mkv,*.mp4,*.avi,*.m4v,*.mov,*.ts,*.vob,*.webm*.mp3,*.mp2,*.ogg,*.flac,*.m4a,*.srt,*.sub,*.ass,*.idx,*.smi`|
| IGNORE_FILES        | Comma separated list of file patterns to ignore                         | `""`                              |


### Running locally

1. Clone the repo:

```bash
git clone https://github.com/EdouardRouch/tidewatcher.git
cd tidewatcher/app
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r ../requirements.txt
```

4. Create `.env` file in root folder with your config.

5. Run the script:

```bash
python tidewatcher.py
```

---

### Using Docker-Compose

```bash
services:
  tidewatcher:
    image: edouardrouch/tidewatcher:latest
    container_name: tidewatcher
    environment:
      - JELLYFIN_URL=http://192.168.178.252:8096
      - JELLYFIN_API_KEY=your api key
      - LOG_TO_FILE=false
      - LOG_TO_STDOUT=true
      - DELAY_SECONDS=60
      - POLL_TIMEOUT=5
      - TZ=Europe/Paris
    volumes:
      - /mnt/jellyfin:/data:ro   # Replace with your actual media library folder (read-only)
      - ./logs:/var/log          # Local folder for logs if LOG_TO_FILE is true
    restart: unless-stopped

```

## Default watched file types

- Video: `.mkv`, `.mp4`, `.avi`, `.m4v`, `.mov`, `.ts`, `.vob`, `.webm`
- Audio: `.mp3`, `.mp2`, `.ogg`, `.flac`, `.m4a`
- Subtitles: `.srt`, `.sub`, `.ass`, `.idx`, `.smi`


## License

MIT License


## Contributing

Feel free to open issues or pull requests to improve tidewatcher.

---

FROM python:3.14-slim@sha256:35f442c69294267a391b05d9526b6a330986ad9b008152a2e24257a1f98a8dc0

WORKDIR /app

COPY app/tidewatcher.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "tidewatcher.py"]
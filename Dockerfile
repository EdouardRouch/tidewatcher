FROM python:3.14-slim@sha256:9b9a75b908891c42b7af174dcf3f6534ebcedfc28c874c6281eb452e86470e3e

WORKDIR /app

COPY app/tidewatcher.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "tidewatcher.py"]
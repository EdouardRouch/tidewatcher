FROM python:3.14-slim@sha256:0c6bb259d537411417dd3b0052730e237ec0b8bd66aeaf64f1804a142d5c23ae

WORKDIR /app

COPY app/tidewatcher.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "tidewatcher.py"]
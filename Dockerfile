FROM python:3.14-slim@sha256:a86d0ed368c9f7572ef6a7d0b847e8d5a927ea4123bb5ea335f206702a0fa40d

WORKDIR /app

COPY app/tidewatcher.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "tidewatcher.py"]
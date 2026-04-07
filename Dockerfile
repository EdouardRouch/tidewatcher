FROM python:3.14-slim@sha256:6869258bd3dd1e6947f4e9a375319809cd02f29312ed70aabe98d8086905cfd4

WORKDIR /app

COPY app/tidewatcher.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "tidewatcher.py"]
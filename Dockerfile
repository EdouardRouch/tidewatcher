FROM python:3.14-slim@sha256:0097bb60d0c7a2c6af5a56e747eabc2016218f837f76daa70b9526fb883bc499

WORKDIR /app

COPY app/tidewatcher.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "tidewatcher.py"]
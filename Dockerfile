FROM python:3.14-slim@sha256:4ed33101ee7ec299041cc41dd268dae17031184be94384b1ce7936dc4e5dead3

WORKDIR /app

COPY app/tidewatcher.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "tidewatcher.py"]
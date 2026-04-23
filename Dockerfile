FROM python:3.14-slim@sha256:3989a23fd2c28a34c7be819e488b958a10601d421ac25bea1e7a5d757365e2d5

WORKDIR /app

COPY app/tidewatcher.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "tidewatcher.py"]
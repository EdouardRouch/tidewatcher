FROM python:3.14-slim@sha256:cfbffff88b668d1c11745222fe2303c70db095d57e13daa0d18f294c2154563d

WORKDIR /app

COPY app/tidewatcher.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "tidewatcher.py"]
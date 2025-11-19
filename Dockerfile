FROM python:3.14-slim@sha256:119fd5bd9c01a9283d0be29d31218fb04f4575c67b3e89151417d61f6e1a6f58

WORKDIR /app

COPY app/tidewatcher.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "tidewatcher.py"]
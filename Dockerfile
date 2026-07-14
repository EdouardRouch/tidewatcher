FROM python:3.14-slim@sha256:072ffcb57bab690052d9b695592d811a42b849e8ef254ced334a28f283d5f76a

WORKDIR /app

COPY app/tidewatcher.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "tidewatcher.py"]
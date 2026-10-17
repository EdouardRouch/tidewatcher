FROM python:3.15-slim@sha256:d802f03223b9e00604cd54574bcac1a4638914c43683d3f0afd6ebee35f25313

WORKDIR /app

COPY app/tidewatcher.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "tidewatcher.py"]
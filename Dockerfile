FROM python:3.14-slim@sha256:3fa9f1158b0d8b5029c357770bd522e7955546ffc5db885d8b366ec4a687afd4

WORKDIR /app

COPY app/tidewatcher.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "tidewatcher.py"]
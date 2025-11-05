FROM python:3.14-slim@sha256:e3782138420d9e87c16497320817db6ca8689e354d6150426dd6fc261f3fd682

WORKDIR /app

COPY app/tidewatcher.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "tidewatcher.py"]
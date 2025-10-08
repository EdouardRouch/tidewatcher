FROM python:3.11-slim@sha256:9bffe4353b925a1656688797ebc68f9c525e79b1d377a764d232182a519eeec4

WORKDIR /app

COPY app/tidewatcher.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "tidewatcher.py"]
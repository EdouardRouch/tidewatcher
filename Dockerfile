FROM python:3.14-slim@sha256:b0c4ec81396588a94b99052caf2f786e6e92e03111991d3d40c68762ee48d2ab

WORKDIR /app

COPY app/tidewatcher.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "tidewatcher.py"]
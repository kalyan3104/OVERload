FROM python:3.10-slim

WORKDIR /app

# system deps
RUN apt-get update && apt-get install -y build-essential git wget libsndfile1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app

ENV PYTHONUNBUFFERED=1
CMD ["bash", "start.sh"]

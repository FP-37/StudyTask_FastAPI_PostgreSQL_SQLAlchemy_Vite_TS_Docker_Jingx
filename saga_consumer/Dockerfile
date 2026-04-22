FROM python:3.12-slim

WORKDIR /app

COPY saga_consumer/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY saga_consumer /app

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]

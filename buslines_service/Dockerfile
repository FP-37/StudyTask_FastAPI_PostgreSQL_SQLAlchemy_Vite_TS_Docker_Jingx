FROM python:3.12-slim

WORKDIR /app

COPY buslines_service/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY buslines_service/buslines_app /app/buslines_app
COPY shared /app/shared

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "buslines_app.main:app", "--host", "0.0.0.0", "--port", "8000"]

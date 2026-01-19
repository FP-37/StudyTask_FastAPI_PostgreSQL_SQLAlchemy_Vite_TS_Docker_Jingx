FROM python:3.12-slim

WORKDIR /app

COPY auth_service/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY auth_service/auth_app /app/auth_app
COPY shared /app/shared

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 8001
CMD ["python", "-m", "uvicorn", "auth_app.main:app", "--host", "0.0.0.0", "--port", "8001"]

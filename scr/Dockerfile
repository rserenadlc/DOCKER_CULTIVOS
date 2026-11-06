FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY scr/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el contenido del proyecto para tener acceso a scr dislexia y model
COPY . /app

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "scr.app:app", "--host", "0.0.0.0", "--port", "8000"]

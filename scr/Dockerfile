FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente y las carpetas de modelos
COPY . /app/scr
COPY ../model /app/model

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "scr.app:app", "--host", "0.0.0.0", "--port", "8000"]

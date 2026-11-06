FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copiar requirements.txt directamente desde la raíz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código al contenedor
COPY . /app

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "scr.app:app", "--host", "0.0.0.0", "--port", "8000"]

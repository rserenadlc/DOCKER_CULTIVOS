FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY frontend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos especificando la ruta desde el contexto raíz
COPY frontend/app.py .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

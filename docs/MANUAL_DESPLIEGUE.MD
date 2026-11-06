# Manual de Despliegue en la Nube y Guía Técnica

## 1. Requerimientos Técnicos
- Docker Engine v24+ y Docker Compose v2+
- Python 3.10+
- Cuenta activa en plataforma PaaS (Render, AWS App Runner o GCP Cloud Run)

## 2. Estrategia de Despliegue en Nube (PaaS)
Se selecciona **Render / AWS App Runner** por soporte nativo de `docker-compose` y contenedores Docker independientes:
1. **Contenedor Backend (FastAPI):** Exposición del puerto `8000`. Carga del modelo en memoria durante el boot.
2. **Contenedor Frontend (Streamlit):** Exposición del puerto `8501`. Comunicación interna mediante variable de entorno `API_URL`.
### Registros Públicos de Imágenes (Docker Hub)
- **Imagen Backend:** `https://hub.docker.com/r/richarddees/cultivos-backend`
  - Comando de descarga: `docker pull richarddees/cultivos-backend:v1`
- **Imagen Frontend:** `https://hub.docker.com/r/richarddees/cultivos-frontend`
  - Comando de descarga: `docker pull richarddees/cultivos-frontend:v1`

## 3. Guía Paso a Paso para Despliegue Cloud (vía Container Registry)
1. **Construir e etiquetar imágenes localmente:**
   ```bash
   docker build -t tu_usuario/cultivos-backend:v1 -f scr/Dockerfile .
   docker build -t tu_usuario/cultivos-frontend:v1 -f frontend/Dockerfile .

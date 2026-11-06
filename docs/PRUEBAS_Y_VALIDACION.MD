# Reporte de Pruebas y Validación del Sistema

Este documento registra la batería de pruebas ejecutadas sobre la API (FastAPI) y la interfaz (Streamlit) para garantizar estabilidad, resiliencia y manejo adecuado de casos extremos.

## 1. Matriz de Pruebas Funcionales y Casos Extremos

| ID | Tipo de Prueba | Entrada de Prueba | Comportamiento / Resultado Esperado | Resultado Obtenido | Estatus |
|---|---|---|---|---|---|
| **PR-01** | Funcional (Valida) | Ciudad: `Córdoba`, País: `México` | HTTP 200. Geocodificación exitosa, clima ~20°C, Top 1: Coffee. | HTTP 200, 89% Similitud Coffee | **PASÓ** |
| **PR-02** | Funcional (Valida) | Ciudad: `Veracruz`, País: `México` | HTTP 200. Clima de costa ~24°C, Top 1: Maize. | HTTP 200, 74% Similitud Maize | **PASÓ** |
| **PR-03** | Caso Extremo (Ciudad Inexistente) | Ciudad: `CiudadFantasmas123`, País: `México` | HTTP 404 manejado. Mensaje explicativo en UI sin colapsar el contenedor. | HTTP 404: "No pudimos encontrar las coordenadas" | **PASÓ** |
| **PR-04** | Caso Extremo (Texto Vacío) | Ciudad: `""`, País: `México` | Validación previa en cliente (Streamlit). Muestra aviso de advertencia sin enviar request. | Advertencia en UI activada | **PASÓ** |
| **PR-05** | Resiliencia (Timeout Geocodificador) | Simulación de caída de API Nominatim | HTTP 504 Timeout manejado en API y capturado por la interfaz. | HTTP 504 handled | **PASÓ** |
| **PR-06** | Contenerización (Salud) | GET `http://localhost:8000/health` | HTTP 200: `{"status": "ok"}` desde el contenedor Docker backend. | HTTP 200 OK | **PASÓ** |

## 2. Análisis del Comportamiento del Modelo
- **Sensibilidad Climática:** El modelo responde dinámicamente a la altitud y gradiente térmico de la región. En Córdoba (más fresco y húmedo) predice Café[cite: 11], mientras que en el puerto de Veracruz (más cálido) prioriza Maíz[cite: 10].
- **Manejo de Errores en Capas:** Las validaciones de Pydantic y los bloques `try-except` evitan que peticiones malformadas causen la caída del contenedor (`exit status 1`).

import streamlit as st
import requests
import os

# 1. Configuración general de la página
st.set_page_config(
    page_title="Recomendador de Cultivos IA",
    page_icon="🌱",
    layout="centered"
)

# 2. Variable de entorno para la conexión con el Backend
# Localmente apuntará al puerto 8000. En Docker, usará el nombre del servicio.
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("Recomendador Inteligente de Cultivos")
st.markdown("""
Este sistema utiliza un modelo de **Machine Learning (Random Forest)** para recomendar los mejores cultivos 
basándose en las condiciones climáticas y de suelo de tu región.

Ingresa tu ciudad y nuestra IA buscará los datos espaciales globales para darte un Top 3 de opciones.
""")

st.divider()

# 3. Formulario de captura
col1, col2 = st.columns(2)
with col1:
    ciudad = st.text_input("Ciudad o Municipio", placeholder="Ej. Veracruz")
with col2:
    pais = st.text_input("País", value="México")

if st.button("Buscar Recomendación", type="primary"):
    if not ciudad.strip():
        st.warning("Por favor, ingresa una ciudad para continuar.")
    else:
        with st.spinner("Geolocalizando y analizando el clima..."):
            try:
                # 4. Petición POST a tu API FastAPI
                payload = {"ciudad": ciudad, "pais": pais}
                response = requests.post(f"{API_URL}/predict_by_city", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("¡Análisis completado con éxito!")
                    
                    # Mostrar Ubicación Detectada
                    st.subheader("📍Ubicación Localizada")
                    st.info(data["ubicacion_detectada"]["direccion"])
                    
                    # Mostrar Condiciones Ambientales usando métricas visuales
                    st.subheader("Condiciones Estimadas")
                    condiciones = data["condiciones_estimadas"]
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Temperatura Anual", condiciones["temperatura_anual"])
                    c2.metric("Lluvia Anual", condiciones["lluvia_anual"])
                    c3.metric("pH del Suelo", str(condiciones["ph_suelo"]))
                    
                    # Mostrar Recomendaciones Top 3
                    st.subheader("Top 3 Cultivos Recomendados")
                    recomendaciones = data["recomendaciones_top3"]
                    
                    for i, rec in enumerate(recomendaciones):
                        porcentaje = float(rec['probabilidad'].replace('%', ''))
                        st.write(f"**{i+1}. {rec['cultivo'].capitalize()}**")
                        # Barra de progreso visual para la probabilidad
                        st.progress(int(porcentaje) / 100, text=f"Similitud ambiental: {rec['probabilidad']}")
                        
                else:
                    # 5. Manejo de Errores (Casos Extremos de la rúbrica)
                    error_msg = response.json().get("detail", "Error desconocido en el servidor.")
                    st.error(f"Error {response.status_code}: {error_msg}")
                    
            except requests.exceptions.ConnectionError:
                st.error("No se pudo conectar con la API. Asegúrate de que el backend (FastAPI) está en ejecución.")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import numpy as np
from scipy.spatial import KDTree
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

app = FastAPI(title="Recomendador Inteligente de Cultivos (Geo-Grounded)")

# 1. Inicializar geolocalizador (fuera del try para que siempre exista)
geolocator = Nominatim(user_agent="app_cultivos_tecmilenio")

# 2. Cargar el Modelo y la Base de Datos Espacial
try:
    model = joblib.load("../model/crop_model_geo.pkl")
    spatial_db = pd.read_csv("../model/spatial_database.csv")
    
    coordenadas = spatial_db[['lat', 'lon']].values
    arbol_espacial = KDTree(coordenadas)
    features_cols = spatial_db.columns.drop(['lat', 'lon'])
except Exception as e:
    print(f"ATENCIÓN - Error cargando el modelo: {e}")
    # Si ves este error en la terminal, necesitas ejecutar train.py

# 2. Esquema de entrada de datos
class LocationInput(BaseModel):
    ciudad: str
    pais: str = "Mexico" # Valor por defecto

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API y Modelo cargados correctamente"}

@app.post("/predict_by_city")
def predict_crop(location: LocationInput):
    # A. Buscar Latitud y Longitud de la ciudad
    lugar_texto = f"{location.ciudad}, {location.pais}"
    try:
        geo_info = geolocator.geocode(lugar_texto, timeout=5)
        if not geo_info:
            raise HTTPException(status_code=404, detail="No pudimos encontrar las coordenadas de esa ciudad. Intenta con otra cercana.")
    except GeocoderTimedOut:
        raise HTTPException(status_code=504, detail="El servicio de mapas tardó mucho en responder.")

    lat_usuario = geo_info.latitude
    lon_usuario = geo_info.longitude

    # B. Buscar el clima y suelo más parecido en nuestra base de datos (Nearest Neighbor)
    distancia, indice_cercano = arbol_espacial.query([[lat_usuario, lon_usuario]])
    fila_cercana = spatial_db.iloc[indice_cercano[0]]
    
    # C. Extraer las 16 características ambientales de ese punto
    features_ambientales = fila_cercana[features_cols].values.reshape(1, -1)
    
    # D. Hacer la predicción (Obtener el Top 3 de probabilidades)
    probabilidades = model.predict_proba(features_ambientales)[0]
    clases_modelo = model.classes_
    
    # Ordenar índices de mayor a menor probabilidad
    top_3_indices = np.argsort(probabilidades)[::-1][:3]
    
    resultados_top3 = []
    for idx in top_3_indices:
        resultados_top3.append({
            "cultivo": clases_modelo[idx],
            "probabilidad": f"{probabilidades[idx] * 100:.1f}%"
        })

    return {
        "status": "success",
        "ubicacion_detectada": {
            "direccion": geo_info.address,
            "latitud": lat_usuario,
            "longitud": lon_usuario
        },
        "condiciones_estimadas": {
            "temperatura_anual": f"{fila_cercana['temperature']} °C",
            "lluvia_anual": f"{fila_cercana['rainfall']} mm/yr",
            "ph_suelo": round(fila_cercana['ph'], 2)
        },
        "recomendaciones_top3": resultados_top3
    }

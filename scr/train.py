import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

print("Cargando datasets...")
# Cargar ambos CSV (Ajusta la ruta según donde los hayas guardado)
df_geo = pd.read_csv('../data/crop_recommendation_geo.csv')
df_loc = pd.read_csv('../data/crop_locations.csv')

# Unir ambos dataframes por 'id', ignorando el 'label' duplicado del segundo archivo
df_full = pd.merge(df_geo, df_loc.drop(columns=['label']), on='id')

# Seleccionar las 16 características ambientales (Omitimos lat, lon, etc.)
features = [
    'N', 'P', 'exch_bases', 'ph', 'soc', 'clay', 'sand', 'cec', 
    'temperature', 'temp_min_month', 'temp_max_month', 'humidity', 
    'rainfall', 'rain_seasonality', 'solar_radiation', 'elevation'
]

X = df_full[features]
y = df_full['label']

print("Entrenando Random Forest (esto puede tomar un momento)...")
model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X, y)

# Crear directorio model si no existe
os.makedirs('../model', exist_ok=True)

# 1. Guardar el modelo entrenado
joblib.dump(model, '../model/crop_model_geo.pkl')

# 2. Guardar una base de datos espacial limpia para la API (solo Lat, Lon y Features)
db_espacial = df_full[['lat', 'lon'] + features]
db_espacial.to_csv('../model/spatial_database.csv', index=False)

print("¡Modelo y base de datos espacial guardados con éxito!")

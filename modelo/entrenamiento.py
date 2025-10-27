import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
from utils.features import extraer_caracteristicas

# Carga los datos
df = pd.read_csv("modelo/datos.csv")
# Filtra las URLs que dieron error en VirusTotal (etiqueta -1)
df = df[df["label"] != -1] 

# Extrae características de las URLs
X_text = df["url"]
X = [extraer_caracteristicas(url) for url in X_text] 
y = df["label"]

# Entrena el modelo
modelo = RandomForestClassifier()
modelo.fit(X, y)

# Guarda el modelo entrenado
joblib.dump(modelo, "modelo/modelo_phishing.pkl")
print("✅ Modelo entrenado y guardado.")

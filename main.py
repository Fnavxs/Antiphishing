---
### ARCHIVO: `main.py`
```python
import pandas as pd
import joblib
import os
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from utils.features import extraer_caracteristicas
from utils.virustotal import verificar_virustotal

# --- Configuración de la App ---
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- Carga del Modelo ---
modelo_path = "modelo/modelo_phishing.pkl"
modelo = joblib.load(modelo_path)

def reentrenar_y_recargar():
    """
    Función para ejecutar el entrenamiento en segundo plano
    y luego recargar el modelo en la variable global.
    """
    print("Iniciando re-entrenamiento en segundo plano...")
    import subprocess
    subprocess.run(["python", "modelo/entrenamiento.py"])
    
    # Recargamos el modelo en la variable global
    global modelo
    modelo = joblib.load(modelo_path)
    print("✅ Modelo recargado en memoria.")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/verificar")
async def verificar(url: str, background_tasks: BackgroundTasks):
    df = pd.read_csv("modelo/datos.csv")
    
    # Comprobar si la URL ya existe en nuestro dataset
    if url not in df["url"].values:
        # --- URL NUEVA ---
        # 1. Verificamos con VirusTotal
        etiqueta = verificar_virustotal(url) # 1: maliciosa, 0: legítima, -1: desconocida
        
        # 2. Si VirusTotal dio una respuesta, la guardamos y re-entrenamos
        if etiqueta != -1:
            nueva_fila = pd.DataFrame([[url, etiqueta]], columns=["url", "label"])
            df = pd.concat([df, nueva_fila], ignore_index=True)
            df.to_csv("modelo/datos.csv", index=False)
            
            # 3. Añadimos el re-entrenamiento como tarea de fondo
            background_tasks.add_task(reentrenar_y_recargar)

        # 4. Devolvemos el resultado de VirusTotal INMEDIATAMENTE
        adv = "⚠️ Este enlace podría ser peligroso (según VirusTotal)" if etiqueta == 1 else \
              "✅ No parece fraudulento (según VirusTotal)" if etiqueta == 0 else \
              "❓ No se pudo confirmar con VirusTotal"
        
        mod_ia = "Fraudulento (vía VT)" if etiqueta == 1 else "Legítimo (vía VT)" if etiqueta == 0 else "Dudoso (vía VT)"
        
        resultado = {
            "url": url,
            "modelo_ia": mod_ia,
            "advertencia": adv
        }
    
    else:
        # --- URL CONOCIDA ---
        # 1. Usamos nuestro modelo de IA (que ya fue entrenado con esta URL)
        caracteristicas = extraer_caracteristicas(url)
        prediccion = modelo.predict([caracteristicas])[0]

        resultado = {
            "url": url,
            "modelo_ia": "Fraudulento" if prediccion == 1 else "Legítimo" if prediccion == 0 else "Dudoso",
            "advertencia": "⚠️ Este enlace podría ser peligroso" if prediccion == 1 else \
                           "✅ No parece fraudulento" if prediccion == 0 else \
                           "❓ No se puede confirmar"
        }
    
    return resultado

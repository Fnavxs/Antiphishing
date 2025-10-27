import requests
from bs4 import BeautifulSoup
import pandas as pd

def safe_request(url):
    """Función helper para hacer requests con manejo de errores."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Lanza error si es 4xx o 5xx
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"Error al hacer scraping de {url}: {e}")
        return None

def extraer_urls_osi():
    """Extrae URLs de avisos de seguridad de la OSI."""
    url = "https://www.osi.es/es/actualidad/avisos-de-seguridad"
    soup = safe_request(url)
    urls_detectadas = []
    
    if soup:
        # Selector de la imagen: 'div.view-content a'
        for enlace in soup.select("div.view-content a"):
            href = enlace.get("href")
            # Nos aseguramos de que es un enlace completo y no relativo
            if href and href.startswith("http"):
                urls_detectadas.append(href)
                
    return list(set(urls_detectadas)) # Devuelve solo URLs únicas

def extraer_urls_incibe():
    """Extrae URLs de avisos de seguridad de INCIBE."""
    url = "https://www.incibe.es/protege-tu-empresa/avisos-seguridad"
    soup = safe_request(url)
    urls_detectadas = []
    
    if soup:
        # Selector de la imagen: 'div.views-field-title a'
        for enlace in soup.select("div.views-field-title a"):
            href = enlace.get("href")
            if href and href.startswith("http"):
                urls_detectadas.append(href)
            # A veces los enlaces son relativos
            elif href and href.startswith("/"):
                urls_detectadas.append(f"https://www.incibe.es{href}")
                
    return list(set(urls_detectadas)) # Devuelve solo URLs únicas

def anadir_urls_al_dataset(urls, etiqueta=1):
    """Añade una lista de URLs al dataset si no existen."""
    df_path = "modelo/datos.csv"
    try:
        df = pd.read_csv(df_path)
    except FileNotFoundError:
        print(f"Archivo no encontrado en {df_path}, creando uno nuevo.")
        df = pd.DataFrame(columns=["url", "label"])
        
    nuevas_urls = [url for url in urls if url not in df["url"].values]
    
    if nuevas_urls:
        nuevas_filas = pd.DataFrame(
            [[url, etiqueta] for url in nuevas_urls],
            columns=["url", "label"]
        )
        df = pd.concat([df, nuevas_filas], ignore_index=True)
        df.to_csv(df_path, index=False)
        print(f"✅ Añadidas {len(nuevas_urls)} URLs nuevas al dataset.")
    else:
        print("ℹ️ No hay URLs nuevas para añadir.")

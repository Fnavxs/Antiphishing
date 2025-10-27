import requests
import os
import base64
from dotenv import load_dotenv

# Carga las variables de entorno (busca el archivo .env)
load_dotenv()

# Lee la API Key desde las variables de entorno
API_KEY = os.environ.get("VT_API_KEY")
if not API_KEY:
    print("Error: No se encontró la variable de entorno VT_API_KEY.")
    print("Asegúrate de crear un archivo .env con tu clave.")
    API_KEY = "TU_CLAVE_POR_DEFECTO_SI_FALLA" # Fallback

def get_url_id(url):
    """Codifica la URL en Base64 para la API v3 de VirusTotal."""
    # .strip("=") es importante para que la API de VT lo acepte
    return base64.urlsafe_b64encode(url.encode()).decode().strip("=")

def verificar_virustotal(url):
    """
    Obtiene el reporte existente de VirusTotal para una URL.
    Retorna: 1 (maliciosa), 0 (legítima), -1 (desconocida/error).
    """
    url_id = get_url_id(url)
    vt_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
    headers = {"x-apikey": API_KEY}
    
    try:
        response = requests.get(vt_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # Obtenemos las estadísticas del *último* análisis
            stats = data["data"]["attributes"]["last_analysis_stats"]
            
            if stats["malicious"] > 0:
                return 1 # Es maliciosa
            else:
                return 0 # No se detectó como maliciosa
        
        elif response.status_code == 404:
            # La URL no se encuentra en VirusTotal.
            print(f"URL no encontrada en VT: {url}")
            return -1 # Desconocida
        
        else:
            # Otro error de API (límite de cuota, etc.)
            print(f"Error de API VirusTotal: {response.status_code}")
            return -1 # Desconocida/Error
            
    except requests.RequestException as e:
        # Error de red (timeout, no se puede conectar, etc.)
        print(f"Error de red al contactar VirusTotal: {e}")
        return -1 # Desconocida/Error

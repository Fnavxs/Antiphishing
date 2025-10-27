from utils.fuentes_espanolas import extraer_urls_osi, extraer_urls_incibe, anadir_urls_al_dataset
import subprocess

print("Buscando URLs en OSI...")
urls_osi = extraer_urls_osi()
print(f"Encontradas {len(urls_osi)} URLs en OSI.")

print("Buscando URLs en INCIBE...")
urls_incibe = extraer_urls_incibe()
print(f"Encontradas {len(urls_incibe)} URLs en INCIBE.")

todas_urls = list(set(urls_osi + urls_incibe))
print(f"Total de {len(todas_urls)} URLs únicas encontradas.")

if todas_urls:
    # Añadimos las URLs al dataset con la etiqueta 1 (maliciosas)
    anadir_urls_al_dataset(todas_urls, etiqueta=1)
    
    # Ejecutamos el entrenamiento
    print("Ejecutando entrenamiento del modelo...")
    subprocess.run(["python", "modelo/entrenamiento.py"])
    print("✅ Modelo actualizado con fuentes españolas.")
else:
    print("ℹ️ No se encontraron nuevas URLs en las fuentes.")

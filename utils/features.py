from urllib.parse import urlparse

def extraer_caracteristicas(url):
    partes = urlparse(url)
    
    return [
        len(url),
        url.count("."),
        partes.netloc.count("-"),
        int(url.startswith("https")),
        int("@" in url),
        int("login" in url.lower()),
        int("secure" in url.lower()),
        int("paypal" in url.lower())
    ]

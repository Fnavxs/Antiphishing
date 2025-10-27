async function verificar() {
    const urlInput = document.getElementById("urlInput");
    const url = urlInput.value;
    const resultadoDiv = document.getElementById("resultado");

    // Limpiar resultado anterior
    resultadoDiv.innerHTML = "";

    if (!url) {
        resultadoDiv.innerHTML = "<p>Por favor, introduce una URL.</p>";
        return;
    }

    // Mostrar un indicador de carga
    resultadoDiv.innerHTML = "<p>Verificando...</p>";

    try {
        const response = await fetch(`/verificar?url=${encodeURIComponent(url)}`);
        if (!response.ok) {
            throw new Error(`Error del servidor: ${response.status}`);
        }
        
        const data = await response.json();

        // 🛡️ Prevenir XSS: Crear elementos y asignar con textContent
        resultadoDiv.innerHTML = ""; // Limpiar el "Verificando..."

        // 1. URL
        const pUrl = document.createElement("p");
        const strongUrl = document.createElement("strong");
        strongUrl.textContent = data.url; // ¡SEGURO!
        pUrl.appendChild(document.createTextNode("URL: "));
        pUrl.appendChild(strongUrl);
        
        // 2. Veredicto IA
        const pVeredicto = document.createElement("p");
        const strongVeredicto = document.createElement("strong");
        strongVeredicto.textContent = data.modelo_ia; // ¡SEGURO!
        
        // Asignar clase para color
        if (data.modelo_ia.includes("Fraudulento")) {
            strongVeredicto.className = "fraudulento";
        } else if (data.modelo_ia.includes("Legítimo")) {
            strongVeredicto.className = "legitimo";
        } else {
            strongVeredicto.className = "dudoso";
        }
        pVeredicto.appendChild(document.createTextNode("Resultado: "));
        pVeredicto.appendChild(strongVeredicto);

        // 3. Advertencia
        const pAdvertencia = document.createElement("p");
        pAdvertencia.textContent = data.advertencia; // ¡SEGURO!
        
        // Añadir todo al div
        resultadoDiv.appendChild(pUrl);
        resultadoDiv.appendChild(pVeredicto);
        resultadoDiv.appendChild(pAdvertencia);

    } catch (error) {
        resultadoDiv.innerHTML = "<p style='color:red;'>Error al contactar con el servidor.</p>";
        console.error("Error en fetch:", error);
    }
}

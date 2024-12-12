// Función para manejar la solicitud al servidor
async function fetchData(endpoint, options) {
    const response = await fetch(endpoint, options);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}

// Función para manejar la actualización de la UI con datos
function updateUI(elementId, content) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = typeof content === "string" ? content : JSON.stringify(content, null, 2);
    }
}

// Función principal que usa las funciones anteriores
function enviar() {
    const endpoint = '/ins_productividad';
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    };

    fetchData(endpoint, options)
        .then(data => {
            console.log("Respuesta:", data);
            updateUI('resultado', data);
        })
        .catch(error => {
            console.error("Error:", error);
            updateUI('resultado', `Error: ${error.message}`);
        });
}

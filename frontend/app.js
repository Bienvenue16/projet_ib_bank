// URL de ton backend (À changer plus tard pour l'URL Render)
const API_URL = "http://127.0.0.1:5000/chat";

async function sendMessage() {
    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const message = input.value.trim();

    if (!message) return;

    // 1. Afficher le message de l'utilisateur
    appendMessage('user', message);
    input.value = "";

    // 2. Afficher un indicateur de chargement
    const loadingId = "loading-" + Date.now();
    chatBox.innerHTML += `<div class="msg bot" id="${loadingId}"><i>IB Bank écrit...</i></div>`;
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        // 3. Appel API vers le Backend Flask
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();
        
        // Supprimer l'indicateur de chargement
        document.getElementById(loadingId).remove();

        if (data.reply) {
            appendMessage('bot', data.reply);
        } else {
            appendMessage('bot', "Désolé, je rencontre une difficulté technique. Réessayez plus tard.");
        }

    } catch (error) {
        document.getElementById(loadingId).remove();
        appendMessage('bot', "⚠️ Erreur : Impossible de joindre le serveur. Vérifiez que le backend est lancé.");
        console.error("Détails de l'erreur:", error);
    }
}

function appendMessage(role, text) {
    const chatBox = document.getElementById("chat-box");
    const msgDiv = document.createElement("div");
    msgDiv.className = `msg ${role}`;
    msgDiv.innerText = text;
    chatBox.appendChild(msgDiv);
    
    // Scroll automatique vers le bas
    chatBox.scrollTop = chatBox.scrollHeight;
}
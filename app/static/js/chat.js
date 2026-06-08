// Notifications temps réel - polling toutes les 5 secondes
function checkNewMessages() {
    const conversationId = document.querySelector('[data-conversation-id]');
    if (!conversationId) return;

    const id = conversationId.getAttribute('data-conversation-id');
    const messagesList = document.querySelector('.messages-list');
    const lastMessage = messagesList.lastElementChild;
    const lastId = lastMessage ? lastMessage.getAttribute('data-message-id') : 0;

    fetch(/messages/${id}/nouveaux?last_id=${lastId})
        .then(response => response.json())
        .then(data => {
            if (data.messages && data.messages.length > 0) {
                data.messages.forEach(msg => {
                    const div = document.createElement('div');
                    div.className = 'message-item message-autre';
                    div.setAttribute('data-message-id', msg.id);
                    div.innerHTML = `
                        <span class="message-auteur">${msg.prenom} ${msg.nom}</span>
                        <p class="message-contenu">${msg.contenu}</p>
                        <span class="message-date">${msg.created_at}</span>
                    `;
                    messagesList.appendChild(div);
                });
                messagesList.scrollTop = messagesList.scrollHeight;

                // Notification sonore
                const audio = new Audio('/static/sounds/notification.mp3');
                audio.play().catch(() => {});
            }
        })
        .catch(() => {});
}

// Démarrer le polling si on est sur une page de conversation
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.messages-list')) {
        setInterval(checkNewMessages, 5000);
    }
});

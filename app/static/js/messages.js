// Auto-scroll vers le bas des messages
function scrollToBottom() {
    const messagesList = document.querySelector('.messages-list');
    if (messagesList) {
        messagesList.scrollTop = messagesList.scrollHeight;
    }
}

// Soumettre le formulaire avec Entrée
document.addEventListener('DOMContentLoaded', function() {
    scrollToBottom();

    const textarea = document.querySelector('.message-form textarea');
    if (textarea) {
        textarea.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.closest('form').submit();
            }
        });
    }
});

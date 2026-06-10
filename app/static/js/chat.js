const POLL_INTERVAL_MS = 4000;

function scrollToBottom() {
    const list = document.getElementById('messages-list');
    if (list) {
        list.scrollTop = list.scrollHeight;
    }
}

function getLastMessageId() {
    const list = document.getElementById('messages-list');
    if (!list) return 0;
    const items = list.querySelectorAll('[data-message-id]');
    if (!items.length) return 0;
    return parseInt(items[items.length - 1].getAttribute('data-message-id'), 10) || 0;
}

function appendMessage(msg, currentUserId) {
    const list = document.getElementById('messages-list');
    if (!list) return;

    const isMine = msg.expediteur_id === currentUserId;
    const div = document.createElement('div');
    div.className = `message-bubble ${isMine ? 'message-moi' : 'message-autre new-message-badge'}`;
    div.setAttribute('data-message-id', msg.id);

    const auteur = !isMine ? `<span class="message-auteur text-xs font-bold opacity-70">${msg.prenom}</span>` : '';
    const time = msg.created_at ? msg.created_at.substring(11, 16) : '';

    div.innerHTML = `
        ${auteur}
        <p class="message-contenu">${escapeHtml(msg.contenu)}</p>
        <span class="message-date text-xs opacity-60">${time}</span>
    `;
    list.appendChild(div);
    scrollToBottom();
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function checkNewMessages() {
    const container = document.querySelector('[data-conversation-id]');
    if (!container) return;

    const conversationId = container.getAttribute('data-conversation-id');
    const lastId = getLastMessageId();
    const currentUserId = parseInt(container.getAttribute('data-user-id') || '0', 10);

    fetch(`/messages/${conversationId}/nouveaux?last_id=${lastId}`)
        .then((response) => {
            if (!response.ok) throw new Error('poll failed');
            return response.json();
        })
        .then((data) => {
            if (data.messages && data.messages.length > 0) {
                data.messages.forEach((msg) => appendMessage(msg, currentUserId));
            }
        })
        .catch(() => {});
}

function initThemeToggle() {
    const btn = document.getElementById('theme-toggle');
    const darkIcon = document.getElementById('theme-toggle-dark-icon');
    const lightIcon = document.getElementById('theme-toggle-light-icon');
    if (!btn) return;

    const apply = (theme) => {
        if (theme === 'dark') {
            document.documentElement.classList.add('dark');
            lightIcon.classList.remove('hidden');
            darkIcon.classList.add('hidden');
        } else {
            document.documentElement.classList.remove('dark');
            darkIcon.classList.remove('hidden');
            lightIcon.classList.add('hidden');
        }
    };

    const saved = localStorage.getItem('color-theme')
        || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    apply(saved);

    btn.addEventListener('click', () => {
        const isDark = document.documentElement.classList.contains('dark');
        const next = isDark ? 'light' : 'dark';
        localStorage.setItem('color-theme', next);
        apply(next);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    scrollToBottom();

    const container = document.querySelector('[data-conversation-id]');
    if (container) {
        setInterval(checkNewMessages, POLL_INTERVAL_MS);
    }

    const textarea = document.querySelector('.message-form textarea');
    if (textarea) {
        textarea.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                textarea.closest('form').submit();
            }
        });
    }
});

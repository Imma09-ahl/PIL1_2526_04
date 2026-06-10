document.addEventListener('DOMContentLoaded', () => {
    initPasswordToggles();
    initPasswordMatchValidation();
    initFormSubmitFeedback();
});

function initPasswordToggles() {
    const passwordFields = document.querySelectorAll('input[type="password"]');

    passwordFields.forEach((field) => {
        const wrapper = document.createElement('div');
        wrapper.className = 'auth-password-wrapper';
        field.parentNode.insertBefore(wrapper, field);
        wrapper.appendChild(field);

        const toggle = document.createElement('button');
        toggle.type = 'button';
        toggle.className = 'auth-password-toggle';
        toggle.setAttribute('aria-label', 'Afficher le mot de passe');
        toggle.innerHTML = '<span class="material-symbols-outlined text-xl">visibility</span>';

        toggle.addEventListener('click', () => {
            const isPassword = field.type === 'password';
            field.type = isPassword ? 'text' : 'password';
            toggle.innerHTML = isPassword
                ? '<span class="material-symbols-outlined text-xl">visibility_off</span>'
                : '<span class="material-symbols-outlined text-xl">visibility</span>';
        });

        wrapper.appendChild(toggle);
    });
}

function initPasswordMatchValidation() {
    const password = document.getElementById('mot_de_passe');
    const confirm = document.getElementById('confirm_mot_de_passe');

    if (!password || !confirm) {
        return;
    }

    const validate = () => {
        if (confirm.value && password.value !== confirm.value) {
            confirm.setCustomValidity('Les mots de passe ne correspondent pas.');
            confirm.classList.add('auth-field-error');
        } else {
            confirm.setCustomValidity('');
            confirm.classList.remove('auth-field-error');
        }
    };

    password.addEventListener('input', validate);
    confirm.addEventListener('input', validate);
}

function initFormSubmitFeedback() {
    document.querySelectorAll('form').forEach((form) => {
        form.addEventListener('submit', () => {
            const button = form.querySelector('button[type="submit"]');
            if (button) {
                button.classList.add('auth-submit-loading');
            }
        });
    });
}

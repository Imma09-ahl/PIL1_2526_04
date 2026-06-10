from functools import wraps

from flask import flash, redirect, session, url_for


def login_required(view):
    """Redirige vers la connexion si l'utilisateur n'est pas authentifié."""
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get('user_id'):
            flash('Veuillez vous connecter pour accéder à cette page.', 'error')
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)
    return wrapped

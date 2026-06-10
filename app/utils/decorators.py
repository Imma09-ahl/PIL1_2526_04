from functools import wraps

from flask import flash, redirect, session, url_for


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get('user_id'):
            flash('Veuillez vous connecter pour accéder au matching.', 'error')
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)
    return wrapped

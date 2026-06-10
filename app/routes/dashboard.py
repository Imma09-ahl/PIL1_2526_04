from flask import Blueprint, redirect, render_template, session, url_for

from app.models.user import get_user_by_id
from app.utils.decorators import login_required

dashboard_bp = Blueprint('dashboard', __name__)


def _profile_completion(user):
    """Calcule le pourcentage de complétion du profil."""
    fields = [
        user.get('filiere'),
        user.get('niveau'),
        user.get('bio'),
    ]
    filled = sum(1 for value in fields if value)
    return int((filled / len(fields)) * 100)


@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    user = get_user_by_id(session['user_id'])
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))

    completion = _profile_completion(user)

    return render_template(
        'dashboard.html',
        user=user,
        completion=completion,
    )

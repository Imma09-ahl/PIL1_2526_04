from flask import Blueprint, flash, redirect, render_template, session, url_for

from app.models.user import get_user_by_id
from app.utils.decorators import login_required

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/profile')
@login_required
def view_profile():
    return redirect(url_for('profile.view_other_profile', user_id=session['user_id']))


@profile_bp.route('/profile/<int:user_id>')
@login_required
def view_other_profile(user_id):
    user = get_user_by_id(user_id)
    if not user:
        flash('Utilisateur non trouvé.', 'error')
        return redirect(url_for('matching.resultats'))

    profile = {
        'user': user,
        'forces': [],
        'faiblesses': [],
        'disponibilites': [],
    }
    return render_template(
        'profile/view.html',
        profile=profile,
        is_own_profile=(user_id == session.get('user_id')),
    )


@profile_bp.route('/profile/edit')
@login_required
def edit_profile():
    flash('Édition du profil disponible après fusion de feature/profil.', 'success')
    return redirect(url_for('matching.resultats'))

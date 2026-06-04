from flask import Blueprint

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile')
def view_profile():
    pass

@profile_bp.route('/profile/edit')
def edit_profile():
    pass
from flask import Blueprint

matching_bp = Blueprint('matching', __name__)

@matching_bp.route('/matching')
def index():
    pass

@matching_bp.route('/matching/resultats')
def resultats():
    pass
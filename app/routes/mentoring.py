from flask import Blueprint

mentoring_bp = Blueprint('mentoring', __name__)

@mentoring_bp.route('/mentoring')
def index():
    pass

@mentoring_bp.route('/mentoring/offres')
def offres():
    pass

@mentoring_bp.route('/mentoring/demandes')
def demandes():
    pass
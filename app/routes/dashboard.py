from flask import Blueprint

competences_bp = Blueprint('competences', __name__)

@competences_bp.route('/competences')
def index():
    pass

@competences_bp.route('/competences/ajouter')
def ajouter():
    pass

@competences_bp.route('/competences/supprimer')
def supprimer():
    pass
from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for

from app.services.matching_service import trouver_matchings
from app.utils.decorators import login_required

matching_bp = Blueprint('matching', __name__)


@matching_bp.route('/matching')
@login_required
def index():
    return redirect(url_for('matching.resultats'))


@matching_bp.route('/matching/resultats')
@login_required
def resultats():
    user_id = session['user_id']
    resultats_list = trouver_matchings(user_id, persister=True)

    return render_template(
        'matching/results.html',
        resultats=resultats_list,
        user_id=user_id,
    )


@matching_bp.route('/matching/api/resultats')
@login_required
def api_resultats():
    user_id = session['user_id']
    resultats_list = trouver_matchings(user_id, persister=False)
    return jsonify({'resultats': resultats_list})

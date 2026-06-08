from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify

from app.services.matching_service import trouver_matchings

matching_bp = Blueprint("matching", __name__)


def _resolve_user_id():
    """
    Récupère l'ID utilisateur sans modifier le module auth :
    - session si déjà disponible
    - sinon ?user_id= pour les tests
    """
    user_id = session.get("user_id")
    if user_id:
        return int(user_id)
    return request.args.get("user_id", type=int)


@matching_bp.route("/matching")
def index():
    """Redirige vers la page de résultats."""
    user_id = _resolve_user_id()
    if not user_id:
        return (
            "Paramètre manquant : ajoutez ?user_id=1 pour tester le matching "
            "(en attendant l'auth).",
            400,
        )
    return redirect(url_for("matching.resultats", user_id=user_id))


@matching_bp.route("/matching/resultats")
def resultats():
    user_id = _resolve_user_id()
    if not user_id:
        return (
            "Paramètre manquant : ajoutez ?user_id=1 pour tester le matching.",
            400,
        )

    resultats_list = trouver_matchings(user_id, persister=True)

    return render_template(
        "matching/results.html",
        resultats=resultats_list,
        user_id=user_id,
    )


@matching_bp.route("/matching/api/resultats")
def api_resultats():
    """Endpoint JSON pour le tri/filtre côté JS."""
    user_id = _resolve_user_id()
    if not user_id:
        return jsonify({"error": "user_id requis"}), 400

    resultats_list = trouver_matchings(user_id, persister=False)
    return jsonify({"resultats": resultats_list})
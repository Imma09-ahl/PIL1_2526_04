from app.models.matching import (
    calculer_score,
    disponibilites_communes,
    matieres_communes,
    save_matching,
)
from app.models.user import get_db

SCORE_MINIMUM = 1.0  # ignorer les matchs quasi nuls


def _get_candidats_mentors(mentore_id):
    """
    Retourne les utilisateurs pouvant être mentors :
    au moins une compétence 'fort' en commun avec une lacune du mentoré.
    """
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT DISTINCT u.id, u.nom, u.prenom, u.photo, u.filiere, u.niveau, u.bio
        FROM utilisateur u
        JOIN competence c_mentor ON c_mentor.utilisateur_id = u.id AND c_mentor.type = 'fort'
        JOIN competence c_mentore ON c_mentore.matiere = c_mentor.matiere
            AND c_mentore.utilisateur_id = %s AND c_mentore.type = 'faible'
        WHERE u.id != %s
        """,
        (mentore_id, mentore_id),
    )
    candidats = cursor.fetchall()
    conn.close()
    return candidats


def construire_resultat(mentor_id, mentore_id):
    """Construit le dictionnaire affiché dans results.html."""
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT id, nom, prenom, photo, filiere, niveau, bio
        FROM utilisateur WHERE id = %s
        """,
        (mentor_id,),
    )
    mentor = cursor.fetchone()
    conn.close()

    if not mentor:
        return None

    score = calculer_score(mentor_id, mentore_id)
    communes = matieres_communes(mentor_id, mentore_id)
    dispos = disponibilites_communes(mentor_id, mentore_id)

    return {
        "utilisateur_id": mentor["id"],
        "nom": mentor["nom"],
        "prenom": mentor["prenom"],
        "photo": mentor.get("photo"),
        "filiere": mentor.get("filiere"),
        "niveau": mentor.get("niveau"),
        "bio": mentor.get("bio"),
        "score": score,
        "matieres_communes": communes,
        "disponibilites_communes": dispos,
        "role": "mentor",
    }


def trouver_matchings(mentore_id, persister=True):
    """
    Cherche les meilleurs mentors pour l'utilisateur connecté (mentoré).
    persister=True : sauvegarde en BDD (évite les doublons via save_matching).
    """
    candidats = _get_candidats_mentors(mentore_id)
    resultats = []

    for candidat in candidats:
        mentor_id = candidat["id"]
        resultat = construire_resultat(mentor_id, mentore_id)

        if not resultat or resultat["score"] < SCORE_MINIMUM:
            continue

        if persister:
            save_matching(mentor_id, mentore_id, resultat["score"])

        resultats.append(resultat)

    return sorted(resultats, key=lambda r: r["score"], reverse=True)
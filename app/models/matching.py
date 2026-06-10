from .user import get_db

# Pondération du score final (total = 100 %)
POIDS_COMPETENCES = 0.50
POIDS_DISPONIBILITES = 0.30
POIDS_PROXIMITE = 0.20


def _get_competences(utilisateur_id, type_competence):
    conn = get_db()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT matiere FROM competence
            WHERE utilisateur_id = %s AND type = %s
            """,
            (utilisateur_id, type_competence),
        )
        rows = cursor.fetchall()
        return [row["matiere"] for row in rows]
    finally:
        conn.close()


def _get_disponibilites(utilisateur_id):
    conn = get_db()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT jour, heure_debut, heure_fin
            FROM disponibilite
            WHERE utilisateur_id = %s
            """,
            (utilisateur_id,),
        )
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()


def _get_utilisateur(utilisateur_id):
    conn = get_db()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, nom, prenom, photo, filiere, niveau, bio
            FROM utilisateur
            WHERE id = %s
            """,
            (utilisateur_id,),
        )
        user = cursor.fetchone()
        return user
    finally:
        conn.close()


def _times_overlap(debut_a, fin_a, debut_b, fin_b):
    """Vérifie le chevauchement de deux créneaux (objets time ou str HH:MM:SS)."""
    return str(debut_a) < str(fin_b) and str(debut_b) < str(fin_a)


def matieres_communes(mentor_id, mentore_id):
    competences_mentor = set(_get_competences(mentor_id, "fort"))
    lacunes_mentore = set(_get_competences(mentore_id, "faible"))
    return sorted(competences_mentor & lacunes_mentore)


def disponibilites_communes(mentor_id, mentore_id):
    dispo_mentor = _get_disponibilites(mentor_id)
    dispo_mentore = _get_disponibilites(mentore_id)
    communes = []

    for dm in dispo_mentor:
        for dme in dispo_mentore:
            if dm["jour"] == dme["jour"] and _times_overlap(
                dm["heure_debut"], dm["heure_fin"],
                dme["heure_debut"], dme["heure_fin"],
            ):
                label = (
                    f"{dm['jour']} "
                    f"{str(dm['heure_debut'])[:5]}–{str(dm['heure_fin'])[:5]}"
                )
                if label not in communes:
                    communes.append(label)

    return communes


def _score_competences(mentor_id, mentore_id):
    communes = matieres_communes(mentor_id, mentore_id)
    lacunes_mentore = _get_competences(mentore_id, "faible")
    if not lacunes_mentore:
        return 0.0
    return (len(communes) / len(lacunes_mentore)) * 100


def _score_disponibilites(mentor_id, mentore_id):
    communes = disponibilites_communes(mentor_id, mentore_id)
    dispo_mentore = _get_disponibilites(mentore_id)
    if not dispo_mentore:
        return 0.0
    return min((len(communes) / len(dispo_mentore)) * 100, 100.0)


def _score_proximite(mentor_id, mentore_id):
  mentor = _get_utilisateur(mentor_id)
  mentore = _get_utilisateur(mentore_id)
  if not mentor or not mentore:
    return 0.0

  score = 0.0
  if mentor.get("filiere") and mentor["filiere"] == mentore.get("filiere"):
    score += 70.0
  if mentor.get("niveau") and mentor["niveau"] == mentore.get("niveau"):
    score += 30.0
  return score


def calculer_score(mentor_id, mentore_id):
    """
    Score de compatibilité 0–100 :
    - 50 % matières (forts mentor ∩ lacunes mentoré)
    - 30 % créneaux horaires communs
    - 20 % filière + niveau
    """
    score_competences = _score_competences(mentor_id, mentore_id)
    score_dispos = _score_disponibilites(mentor_id, mentore_id)
    score_proximite = _score_proximite(mentor_id, mentore_id)

    score_final = (
        POIDS_COMPETENCES * score_competences
        + POIDS_DISPONIBILITES * score_dispos
        + POIDS_PROXIMITE * score_proximite
    )
    return round(score_final, 1)


def save_matching(mentor_id, mentore_id, score):
    """Enregistre ou met à jour un résultat de matching."""
    conn = get_db()
    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id FROM matching
            WHERE mentor_id = %s AND mentore_id = %s
            """,
            (mentor_id, mentore_id),
        )
        existing = cursor.fetchone()

        if existing:
            cursor.execute(
                """
                UPDATE matching SET score = %s
                WHERE mentor_id = %s AND mentore_id = %s
                """,
                (score, mentor_id, mentore_id),
            )
        else:
            cursor.execute(
                """
                INSERT INTO matching (mentor_id, mentore_id, score)
                VALUES (%s, %s, %s)
                """,
                (mentor_id, mentore_id, score),
            )

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()


def get_matchings(utilisateur_id):
    """Historique des matchings où l'utilisateur est mentor ou mentoré."""
    conn = get_db()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT m.*,
                   u1.nom AS nom_mentor, u1.prenom AS prenom_mentor, u1.photo AS photo_mentor,
                   u1.filiere AS filiere_mentor, u1.niveau AS niveau_mentor,
                   u2.nom AS nom_mentore, u2.prenom AS prenom_mentore, u2.photo AS photo_mentore,
                   u2.filiere AS filiere_mentore, u2.niveau AS niveau_mentore
            FROM matching m
            JOIN utilisateur u1 ON m.mentor_id = u1.id
            JOIN utilisateur u2 ON m.mentore_id = u2.id
            WHERE m.mentor_id = %s OR m.mentore_id = %s
            ORDER BY m.score DESC
            """,
            (utilisateur_id, utilisateur_id),
        )
        matchings = cursor.fetchall()
        return matchings
    finally:
        conn.close()
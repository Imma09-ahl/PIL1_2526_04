from .user import get_db


def add_competence(utilisateur_id, matiere, type_comp):
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO competence (utilisateur_id, matiere, type)
            VALUES (%s, %s, %s)
            """,
            (utilisateur_id, matiere, type_comp),
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()


def get_competences(utilisateur_id):
    conn = get_db()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT * FROM competence
            WHERE utilisateur_id = %s
            ORDER BY matiere
            """,
            (utilisateur_id,),
        )
        competences = cursor.fetchall()
        return competences
    finally:
        conn.close()


def delete_competence(competence_id):
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM competence WHERE id = %s', (competence_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()


def delete_competence_for_user(competence_id, utilisateur_id):
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM competence
            WHERE id = %s AND utilisateur_id = %s
            """,
            (competence_id, utilisateur_id),
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()

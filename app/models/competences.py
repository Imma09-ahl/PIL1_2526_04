from .user import get_db

def add_competence(utilisateur_id, matiere, type):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO competence (utilisateur_id, matiere, type)
        VALUES (%s, %s, %s)
    """, (utilisateur_id, matiere, type))
    conn.commit()
    conn.close()

def get_competences(utilisateur_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM competence 
        WHERE utilisateur_id = %s
    """, (utilisateur_id,))
    competences = cursor.fetchall()
    conn.close()
    return competences

def delete_competence(competence_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM competence WHERE id = %s", (competence_id,))
    conn.commit()
    conn.close()

def delete_competence_utilisateur(competence_id, utilisateur_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM competence
        WHERE id = %s AND utilisateur_id = %s
    """, (competence_id, utilisateur_id))
    conn.commit()
    conn.close()

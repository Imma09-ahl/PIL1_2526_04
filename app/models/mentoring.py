from .user import get_db

def create_mentoring(utilisateur_id, type, matiere, format):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO mentoring (utilisateur_id, type, matiere, format)
        VALUES (%s, %s, %s, %s)
    """, (utilisateur_id, type, matiere, format))
    conn.commit()
    conn.close()

def get_all_offres():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT m.*, u.nom, u.prenom, u.filiere 
        FROM mentoring m 
        JOIN utilisateur u ON m.utilisateur_id = u.id
        WHERE m.type = 'offre' AND m.statut = 'ouvert'
    """)
    offres = cursor.fetchall()
    conn.close()
    return offres

def get_all_demandes():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT m.*, u.nom, u.prenom, u.filiere 
        FROM mentoring m 
        JOIN utilisateur u ON m.utilisateur_id = u.id
        WHERE m.type = 'demande' AND m.statut = 'ouvert'
    """)
    demandes = cursor.fetchall()
    conn.close()
    return demandes
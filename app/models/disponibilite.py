from .user import get_db

def add_disponibilite(utilisateur_id, jour, heure_debut, heure_fin):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO disponibilite (utilisateur_id, jour, heure_debut, heure_fin)
        VALUES (%s, %s, %s, %s)
    """, (utilisateur_id, jour, heure_debut, heure_fin))
    conn.commit()
    conn.close()

def get_disponibilites(utilisateur_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM disponibilite
        WHERE utilisateur_id = %s
        ORDER BY FIELD(jour, 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'),
                 heure_debut ASC
    """, (utilisateur_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_disponibilite(disponibilite_id, utilisateur_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM disponibilite
        WHERE id = %s AND utilisateur_id = %s
    """, (disponibilite_id, utilisateur_id))
    conn.commit()
    conn.close()

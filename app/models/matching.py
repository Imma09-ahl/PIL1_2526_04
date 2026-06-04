from .user import get_db

def calculer_score(mentor_id, mentore_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    # Récupérer les compétences du mentor
    cursor.execute("""
        SELECT matiere FROM competence 
        WHERE utilisateur_id = %s AND type = 'fort'
    """, (mentor_id,))
    competences_mentor = [row['matiere'] for row in cursor.fetchall()]
    
    # Récupérer les lacunes du mentoré
    cursor.execute("""
        SELECT matiere FROM competence 
        WHERE utilisateur_id = %s AND type = 'faible'
    """, (mentore_id,))
    lacunes_mentore = [row['matiere'] for row in cursor.fetchall()]
    
    # Calculer le score de compatibilité
    matieres_communes = set(competences_mentor) & set(lacunes_mentore)
    score = len(matieres_communes) / max(len(lacunes_mentore), 1) * 100
    
    conn.close()
    return round(score, 2)

def save_matching(mentor_id, mentore_id, score):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO matching (mentor_id, mentore_id, score)
        VALUES (%s, %s, %s)
    """, (mentor_id, mentore_id, score))
    conn.commit()
    conn.close()

def get_matchings(utilisateur_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT m.*, 
               u1.nom as nom_mentor, u1.prenom as prenom_mentor,
               u2.nom as nom_mentore, u2.prenom as prenom_mentore
        FROM matching m
        JOIN utilisateur u1 ON m.mentor_id = u1.id
        JOIN utilisateur u2 ON m.mentore_id = u2.id
        WHERE m.mentor_id = %s OR m.mentore_id = %s
        ORDER BY m.score DESC
    """, (utilisateur_id, utilisateur_id))
    matchings = cursor.fetchall()
    conn.close()
    return matchings
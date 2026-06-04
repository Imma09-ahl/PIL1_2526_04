from app.models.matching import calculer_score, save_matching
from app.models.user import get_db

def trouver_matchings(utilisateur_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT id FROM utilisateur WHERE id != %s
    """, (utilisateur_id,))
    
    autres_utilisateurs = cursor.fetchall()
    conn.close()
    
    resultats = []
    for autre in autres_utilisateurs:
        score = calculer_score(utilisateur_id, autre['id'])
        if score > 0:
            save_matching(utilisateur_id, autre['id'], score)
            resultats.append({
                'utilisateur_id': autre['id'],
                'score': score
            })
    
    return sorted(resultats, key=lambda x: x['score'], reverse=True)
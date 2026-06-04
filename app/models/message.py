from .user import get_db

def create_conversation(utilisateur1_id, utilisateur2_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO conversation (utilisateur1_id, utilisateur2_id)
        VALUES (%s, %s)
    """, (utilisateur1_id, utilisateur2_id))
    conn.commit()
    conversation_id = cursor.lastrowid
    conn.close()
    return conversation_id

def send_message(conversation_id, expediteur_id, contenu):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO message (conversation_id, expediteur_id, contenu)
        VALUES (%s, %s, %s)
    """, (conversation_id, expediteur_id, contenu))
    conn.commit()
    conn.close()

def get_messages(conversation_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT m.*, u.nom, u.prenom 
        FROM message m
        JOIN utilisateur u ON m.expediteur_id = u.id
        WHERE m.conversation_id = %s
        ORDER BY m.created_at ASC
    """, (conversation_id,))
    messages = cursor.fetchall()
    conn.close()
    return messages

def get_conversations(utilisateur_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.*, 
               u1.nom as nom1, u1.prenom as prenom1,
               u2.nom as nom2, u2.prenom as prenom2
        FROM conversation c
        JOIN utilisateur u1 ON c.utilisateur1_id = u1.id
        JOIN utilisateur u2 ON c.utilisateur2_id = u2.id
        WHERE c.utilisateur1_id = %s OR c.utilisateur2_id = %s
    """, (utilisateur_id, utilisateur_id))
    conversations = cursor.fetchall()
    conn.close()
    return conversations
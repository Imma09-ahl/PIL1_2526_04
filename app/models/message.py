from .user import get_db


def find_or_create_conversation(utilisateur1_id, utilisateur2_id):
    """Retourne une conversation existante ou en crée une nouvelle."""
    if utilisateur1_id == utilisateur2_id:
        return None

    u1, u2 = sorted([utilisateur1_id, utilisateur2_id])

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT id FROM conversation
        WHERE (utilisateur1_id = %s AND utilisateur2_id = %s)
           OR (utilisateur1_id = %s AND utilisateur2_id = %s)
        LIMIT 1
        """,
        (u1, u2, u2, u1),
    )
    existing = cursor.fetchone()

    if existing:
        conn.close()
        return existing['id']

    cursor.execute(
        """
        INSERT INTO conversation (utilisateur1_id, utilisateur2_id)
        VALUES (%s, %s)
        """,
        (utilisateur1_id, utilisateur2_id),
    )
    conn.commit()
    conversation_id = cursor.lastrowid
    conn.close()
    return conversation_id


def create_conversation(utilisateur1_id, utilisateur2_id):
    return find_or_create_conversation(utilisateur1_id, utilisateur2_id)


def get_conversation(conversation_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT c.*,
               u1.nom AS nom1, u1.prenom AS prenom1,
               u2.nom AS nom2, u2.prenom AS prenom2
        FROM conversation c
        JOIN utilisateur u1 ON c.utilisateur1_id = u1.id
        JOIN utilisateur u2 ON c.utilisateur2_id = u2.id
        WHERE c.id = %s
        """,
        (conversation_id,),
    )
    conversation = cursor.fetchone()
    conn.close()
    return conversation


def user_in_conversation(conversation_id, user_id):
    conversation = get_conversation(conversation_id)
    if not conversation:
        return False
    return user_id in (conversation['utilisateur1_id'], conversation['utilisateur2_id'])


def send_message(conversation_id, expediteur_id, contenu):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO message (conversation_id, expediteur_id, contenu)
        VALUES (%s, %s, %s)
        """,
        (conversation_id, expediteur_id, contenu.strip()),
    )
    conn.commit()
    message_id = cursor.lastrowid
    conn.close()
    return message_id


def get_messages(conversation_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT m.*, u.nom, u.prenom
        FROM message m
        JOIN utilisateur u ON m.expediteur_id = u.id
        WHERE m.conversation_id = %s
        ORDER BY m.created_at ASC
        """,
        (conversation_id,),
    )
    messages = cursor.fetchall()
    conn.close()
    return messages


def get_new_messages(conversation_id, last_id=0):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT m.*, u.nom, u.prenom
        FROM message m
        JOIN utilisateur u ON m.expediteur_id = u.id
        WHERE m.conversation_id = %s AND m.id > %s
        ORDER BY m.created_at ASC
        """,
        (conversation_id, last_id),
    )
    messages = cursor.fetchall()
    conn.close()
    return messages


def get_conversations(utilisateur_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT c.*,
               u1.nom AS nom1, u1.prenom AS prenom1,
               u2.nom AS nom2, u2.prenom AS prenom2,
               (
                   SELECT contenu FROM message
                   WHERE conversation_id = c.id
                   ORDER BY created_at DESC LIMIT 1
               ) AS dernier_message,
               (
                   SELECT created_at FROM message
                   WHERE conversation_id = c.id
                   ORDER BY created_at DESC LIMIT 1
               ) AS dernier_message_date
        FROM conversation c
        JOIN utilisateur u1 ON c.utilisateur1_id = u1.id
        JOIN utilisateur u2 ON c.utilisateur2_id = u2.id
        WHERE c.utilisateur1_id = %s OR c.utilisateur2_id = %s
        ORDER BY dernier_message_date DESC, c.created_at DESC
        """,
        (utilisateur_id, utilisateur_id),
    )
    conversations = cursor.fetchall()
    conn.close()
    return conversations

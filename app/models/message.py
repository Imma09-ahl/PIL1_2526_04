from .user import get_db


def find_or_create_conversation(utilisateur1_id, utilisateur2_id):
    """Retourne une conversation existante ou en crée une nouvelle."""
    if utilisateur1_id == utilisateur2_id:
        return None

    u1, u2 = sorted([utilisateur1_id, utilisateur2_id])

    conn = get_db()
    try:
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
        return conversation_id
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()


def create_conversation(utilisateur1_id, utilisateur2_id):
    return find_or_create_conversation(utilisateur1_id, utilisateur2_id)


def get_conversation(conversation_id):
    conn = get_db()
    try:
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
        return conversation
    finally:
        conn.close()


def user_in_conversation(conversation_id, user_id):
    conversation = get_conversation(conversation_id)
    if not conversation:
        return False
    return user_id in (conversation['utilisateur1_id'], conversation['utilisateur2_id'])


def send_message(conversation_id, expediteur_id, contenu, fichier_url=None, fichier_nom=None, type_message='text'):
    conn = get_db()
    try:
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
        return message_id
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()


def mark_messages_as_read(conversation_id, user_id):
    """Marque tous les messages d'une conversation comme lus pour l'utilisateur"""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE message
            SET lu = TRUE
            WHERE conversation_id = %s
            AND expediteur_id != %s
            AND lu = FALSE
            """,
            (conversation_id, user_id),
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()


def delete_message(message_id, user_id):
    """Supprime un message (soft delete en mettant le contenu vide)"""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE message
            SET contenu = '[Message supprimé]'
            WHERE id = %s AND expediteur_id = %s
            """,
            (message_id, user_id),
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()


def update_message(message_id, user_id, new_content):
    """Modifie un message"""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE message
            SET contenu = %s
            WHERE id = %s AND expediteur_id = %s
            """,
            (new_content.strip(), message_id, user_id),
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()


def get_messages(conversation_id):
    conn = get_db()
    try:
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
        return messages
    finally:
        conn.close()


def get_new_messages(conversation_id, last_id=0):
    conn = get_db()
    try:
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
        return messages
    finally:
        conn.close()


def get_conversations(utilisateur_id):
    conn = get_db()
    try:
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
        return conversations
    finally:
        conn.close()

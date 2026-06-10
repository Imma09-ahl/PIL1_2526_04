from flask import current_app
import mysql.connector


def get_db():
    conn = mysql.connector.connect(
        host=current_app.config['MYSQL_HOST'],
        user=current_app.config['MYSQL_USER'],
        port=current_app.config['MYSQL_PORT'],
        password=current_app.config['MYSQL_PASSWORD'],
        database=current_app.config['MYSQL_DB'],
    )
    return conn


def create_user(nom, prenom, email, telephone, mot_de_passe):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO utilisateur (nom, prenom, email, telephone, mot_de_passe)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (nom, prenom, email, telephone, mot_de_passe),
    )
    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM utilisateur WHERE email = %s", (email,))
    user = cursor.fetchone()
    conn.close()
    return user


def get_user_by_telephone(telephone):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM utilisateur WHERE telephone = %s", (telephone,))
    user = cursor.fetchone()
    conn.close()
    return user


def get_user_by_id(user_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM utilisateur WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user


def update_password(user_id, mot_de_passe_hash):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE utilisateur SET mot_de_passe = %s WHERE id = %s",
        (mot_de_passe_hash, user_id),
    )
    conn.commit()
    conn.close()


def update_user(user_id, nom, prenom, email, telephone, filiere, niveau, bio, photo):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE utilisateur
        SET nom = %s, prenom = %s, email = %s, telephone = %s,
            filiere = %s, niveau = %s, bio = %s, photo = %s
        WHERE id = %s
        """,
        (nom, prenom, email, telephone, filiere, niveau, bio, photo, user_id),
    )
    conn.commit()
    conn.close()


def get_user_full_profile(user_id):
    """Résumé profil pour le tableau de bord (sans dépendance aux autres modules)."""
    user = get_user_by_id(user_id)
    if not user:
        return None

    return {
        'user': user,
        'forces': [],
        'faiblesses': [],
        'disponibilites': [],
    }

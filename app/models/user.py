from flask import current_app
import mysql.connector

def get_db():
    conn = mysql.connector.connect(
        host=current_app.config['MYSQL_HOST'],
        user=current_app.config['MYSQL_USER'],
        port=current_app.config['MYSQL_PORT'],
        password=current_app.config['MYSQL_PASSWORD'],
        database=current_app.config['MYSQL_DB']
    )
    return conn

def create_user(nom, prenom, email, telephone, mot_de_passe):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO utilisateur (nom, prenom, email, telephone, mot_de_passe)
        VALUES (%s, %s, %s, %s, %s)
    """, (nom, prenom, email, telephone, mot_de_passe))
    conn.commit()
    conn.close()

def get_user_by_email(email):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM utilisateur WHERE email = %s", (email,))
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


def update_user(user_id, nom, prenom, email, telephone, filiere, niveau, bio, photo):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE utilisateur 
        SET nom = %s, prenom = %s, email = %s, telephone = %s, 
            filiere = %s, niveau = %s, bio = %s, photo = %s
        WHERE id = %s
    """, (nom, prenom, email, telephone, filiere, niveau, bio, photo, user_id))
    conn.commit()
    conn.close()


def get_user_full_profile(user_id):
    """Récupère l'utilisateur + ses compétences"""
    from .competences import get_competences
    
    user = get_user_by_id(user_id)
    if not user:
        return None
    
    competences = get_competences(user_id)
    forces = [c for c in competences if c['type'] == 'fort']
    faiblesses = [c for c in competences if c['type'] == 'faible']
    
    return {
        'user': user,
        'forces': forces,
        'faiblesses': faiblesses,
        'disponibilites': []  # TODO: quand le module dispo sera prêt
    }
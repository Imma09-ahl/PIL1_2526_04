from flask import current_app
import mysql.connector

def get_db():
    conn = mysql.connector.connect(
        host=current_app.config['MYSQL_HOST'],
        user=current_app.config['MYSQL_USER'],
        port=current_app.config.get('MYSQL_PORT', 3306),
        password=current_app.config['MYSQL_PASSWORD'],
        database=current_app.config['MYSQL_DB'],
    )
    return conn


def get_user_by_id(user_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM utilisateur WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user


def update_format_mentorat(user_id, format_mentorat):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE utilisateur SET format_mentorat = %s WHERE id = %s',
        (format_mentorat, user_id),
    )
    conn.commit()
    conn.close()

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
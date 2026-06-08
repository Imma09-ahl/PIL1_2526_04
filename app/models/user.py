from flask import current_app
import mysql.connector

def get_db():
    conn = mysql.connector.connect(
        host=current_app.config['MYSQL_HOST'],
        user=current_app.config['MYSQL_USER'],
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
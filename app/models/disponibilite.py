from datetime import timedelta

from .user import get_db

JOURS_VALIDES = (
    'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'
)


def _format_heure(value):
    if value is None:
        return ''
    if isinstance(value, timedelta):
        total = int(value.total_seconds())
        hours, remainder = divmod(total, 3600)
        minutes, _ = divmod(remainder, 60)
        return f'{hours:02d}:{minutes:02d}'
    if hasattr(value, 'strftime'):
        return value.strftime('%H:%M')
    return str(value)[:5]


def get_disponibilites(utilisateur_id):
    conn = get_db()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, jour, heure_debut, heure_fin
            FROM disponibilite
            WHERE utilisateur_id = %s
            ORDER BY FIELD(jour, 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'),
                     heure_debut
            """,
            (utilisateur_id,),
        )
        rows = cursor.fetchall()
        
        for row in rows:
            row['heure_debut_fmt'] = _format_heure(row['heure_debut'])
            row['heure_fin_fmt'] = _format_heure(row['heure_fin'])
        return rows
    finally:
        conn.close()


def add_disponibilite(utilisateur_id, jour, heure_debut, heure_fin):
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO disponibilite (utilisateur_id, jour, heure_debut, heure_fin)
            VALUES (%s, %s, %s, %s)
            """,
            (utilisateur_id, jour, heure_debut, heure_fin),
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()


def delete_disponibilite(disponibilite_id, utilisateur_id):
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM disponibilite
            WHERE id = %s AND utilisateur_id = %s
            """,
            (disponibilite_id, utilisateur_id),
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()

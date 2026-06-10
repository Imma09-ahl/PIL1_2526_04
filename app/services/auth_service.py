import re
import secrets
import time

from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
EMAIL_PATTERN = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
TELEPHONE_PATTERN = re.compile(r'^(\+229|00229|229)?[0-9]{8,10}$')
RESET_CODE_LENGTH = 6
RESET_CODE_EXPIRY_SECONDS = 15 * 60


def hash_password(mot_de_passe):
    return generate_password_hash(mot_de_passe)


def verify_password(mot_de_passe, mot_de_passe_hash):
    return check_password_hash(mot_de_passe_hash, mot_de_passe)


def validate_register_form(form_data):
    """Valide les données d'inscription. Retourne (errors, form)."""
    form = {
        'nom': (form_data.get('nom') or '').strip(),
        'prenom': (form_data.get('prenom') or '').strip(),
        'email': (form_data.get('email') or '').strip().lower(),
        'telephone': (form_data.get('telephone') or '').strip(),
        'mot_de_passe': form_data.get('mot_de_passe') or '',
        'confirm_mot_de_passe': form_data.get('confirm_mot_de_passe') or '',
    }
    errors = {}

    if not form['nom']:
        errors['nom'] = 'Le nom est obligatoire.'
    if not form['prenom']:
        errors['prenom'] = 'Le prénom est obligatoire.'
    if not form['email']:
        errors['email'] = "L'adresse e-mail est obligatoire."
    elif not EMAIL_PATTERN.match(form['email']):
        errors['email'] = "Le format de l'adresse e-mail est invalide."
    if not form['telephone']:
        errors['telephone'] = 'Le numéro de téléphone est obligatoire.'
    elif not TELEPHONE_PATTERN.match(form['telephone']):
        errors['telephone'] = 'Le format du numéro de téléphone est invalide.'
    if not form['mot_de_passe']:
        errors['mot_de_passe'] = 'Le mot de passe est obligatoire.'
    elif len(form['mot_de_passe']) < 8:
        errors['mot_de_passe'] = 'Le mot de passe doit contenir au moins 8 caractères.'
    if not form['confirm_mot_de_passe']:
        errors['confirm_mot_de_passe'] = 'La confirmation du mot de passe est obligatoire.'
    elif form['mot_de_passe'] != form['confirm_mot_de_passe']:
        errors['confirm_mot_de_passe'] = 'Les mots de passe ne correspondent pas.'

    return errors, form


def validate_login_form(form_data):
    """Valide les données de connexion. Retourne (errors, form)."""
    form = {
        'identifiant': (form_data.get('identifiant') or '').strip(),
        'mot_de_passe': form_data.get('mot_de_passe') or '',
    }
    errors = {}

    if not form['identifiant']:
        errors['identifiant'] = "L'identifiant est obligatoire."
    if not form['mot_de_passe']:
        errors['mot_de_passe'] = 'Le mot de passe est obligatoire.'

    return errors, form


def authenticate_user(identifiant, mot_de_passe):
    """Cherche l'utilisateur par e-mail ou téléphone et vérifie le mot de passe."""
    from app.models.user import get_user_by_email, get_user_by_telephone

    identifiant = identifiant.strip()
    if '@' in identifiant:
        user = get_user_by_email(identifiant.lower())
    else:
        user = get_user_by_telephone(identifiant)

    if user and verify_password(mot_de_passe, user['mot_de_passe']):
        return user
    return None


def generate_reset_code():
    """Génère un code numérique à 6 chiffres."""
    return ''.join(str(secrets.randbelow(10)) for _ in range(RESET_CODE_LENGTH))


def store_reset_code(email, user_id, code):
    """Enregistre le code de réinitialisation en session."""
    session['reset_email'] = email
    session['reset_user_id'] = user_id
    session['reset_code'] = code
    session['reset_expires'] = time.time() + RESET_CODE_EXPIRY_SECONDS


def clear_reset_session():
    """Supprime les données de réinitialisation de la session."""
    session.pop('reset_email', None)
    session.pop('reset_user_id', None)
    session.pop('reset_code', None)
    session.pop('reset_expires', None)


def is_reset_session_active():
    """Vérifie qu'une demande de réinitialisation est en cours et valide."""
    if not session.get('reset_email') or not session.get('reset_code'):
        return False
    return time.time() <= session.get('reset_expires', 0)


def verify_reset_code(code):
    """Vérifie que le code saisi correspond et n'a pas expiré."""
    if not is_reset_session_active():
        return False
    return code == session.get('reset_code')


def validate_forgot_password_form(form_data):
    """Valide la demande de code. Retourne (errors, form)."""
    form = {
        'email': (form_data.get('email') or '').strip().lower(),
    }
    errors = {}

    if not form['email']:
        errors['email'] = "L'adresse e-mail est obligatoire."
    elif not EMAIL_PATTERN.match(form['email']):
        errors['email'] = "Le format de l'adresse e-mail est invalide."

    return errors, form


def validate_reset_password_form(form_data):
    """Valide le code et le nouveau mot de passe. Retourne (errors, form)."""
    form = {
        'code': (form_data.get('code') or '').strip(),
        'mot_de_passe': form_data.get('mot_de_passe') or '',
        'confirm_mot_de_passe': form_data.get('confirm_mot_de_passe') or '',
    }
    errors = {}

    if not form['code']:
        errors['code'] = 'Le code est obligatoire.'
    elif not form['code'].isdigit() or len(form['code']) != RESET_CODE_LENGTH:
        errors['code'] = f'Le code doit contenir {RESET_CODE_LENGTH} chiffres.'
    if not form['mot_de_passe']:
        errors['mot_de_passe'] = 'Le mot de passe est obligatoire.'
    elif len(form['mot_de_passe']) < 8:
        errors['mot_de_passe'] = 'Le mot de passe doit contenir au moins 8 caractères.'
    if not form['confirm_mot_de_passe']:
        errors['confirm_mot_de_passe'] = 'La confirmation du mot de passe est obligatoire.'
    elif form['mot_de_passe'] != form['confirm_mot_de_passe']:
        errors['confirm_mot_de_passe'] = 'Les mots de passe ne correspondent pas.'

    return errors, form

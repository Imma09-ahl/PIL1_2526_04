from flask import Blueprint, flash, redirect, render_template, request, session, url_for
import mysql.connector

from app.models.user import create_user, get_user_by_email, get_user_by_telephone, update_password
from app.services.auth_service import (
    authenticate_user,
    clear_reset_session,
    generate_reset_code,
    hash_password,
    is_reset_session_active,
    store_reset_code,
    validate_forgot_password_form,
    validate_login_form,
    validate_register_form,
    validate_reset_password_form,
    verify_reset_code,
)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    return render_template('index.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id'):
        return redirect(url_for('dashboard.dashboard'))

    if request.method == 'GET':
        return render_template('auth/register.html')

    errors, form = validate_register_form(request.form)

    if not errors.get('email') and get_user_by_email(form['email']):
        errors['email'] = 'Cette adresse e-mail est déjà utilisée.'

    if not errors.get('telephone') and get_user_by_telephone(form['telephone']):
        errors['telephone'] = 'Ce numéro de téléphone est déjà utilisé.'

    if errors:
        return render_template('auth/register.html', errors=errors, form=form)

    try:
        create_user(
            form['nom'],
            form['prenom'],
            form['email'],
            form['telephone'],
            hash_password(form['mot_de_passe']),
        )
    except mysql.connector.IntegrityError:
        flash('Un compte existe déjà avec cet e-mail ou ce numéro de téléphone.', 'error')
        return render_template('auth/register.html', form=form)
    except mysql.connector.Error:
        flash('Impossible de créer le compte pour le moment. Réessayez plus tard.', 'error')
        return render_template('auth/register.html', form=form)

    flash('Inscription réussie ! Vous pouvez maintenant vous connecter.', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('dashboard.dashboard'))

    if request.method == 'GET':
        return render_template('auth/login.html')

    errors, form = validate_login_form(request.form)

    if errors:
        return render_template('auth/login.html', errors=errors, form=form)

    user = authenticate_user(form['identifiant'], form['mot_de_passe'])

    if not user:
        flash('Identifiant ou mot de passe incorrect.', 'error')
        return render_template('auth/login.html', form=form)

    session['user_id'] = user['id']
    session['user_nom'] = user['nom']
    session['user_prenom'] = user['prenom']
    session['user_email'] = user['email']

    flash(f"Bienvenue, {user['prenom']} !", 'success')
    return redirect(url_for('dashboard.dashboard'))


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Vous êtes déconnecté.', 'success')
    return redirect(url_for('auth.index'))


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if session.get('user_id'):
        return redirect(url_for('dashboard.dashboard'))

    if request.method == 'GET':
        return render_template('auth/forgot_password.html')

    errors, form = validate_forgot_password_form(request.form)

    if errors:
        return render_template('auth/forgot_password.html', errors=errors, form=form)

    user = get_user_by_email(form['email'])

    if not user:
        errors['email'] = "Cette adresse n'a pas créé de compte."
        return render_template('auth/forgot_password.html', errors=errors, form=form)

    code = generate_reset_code()
    store_reset_code(form['email'], user['id'], code)

    flash('Un code a été envoyé dans votre boîte e-mail.', 'success')
    return redirect(url_for('auth.reset_password'))


@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if session.get('user_id'):
        return redirect(url_for('dashboard.dashboard'))

    if not is_reset_session_active():
        flash('Votre code a expiré. Veuillez faire une nouvelle demande.', 'error')
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'GET':
        return render_template(
            'auth/reset_password.html',
            email=session['reset_email'],
            dev_code=session.get('reset_code'),
        )

    errors, form = validate_reset_password_form(request.form)

    if errors:
        return render_template(
            'auth/reset_password.html',
            errors=errors,
            form=form,
            email=session['reset_email'],
            dev_code=session.get('reset_code'),
        )

    if not verify_reset_code(form['code']):
        errors['code'] = 'Le code est incorrect ou a expiré.'
        return render_template(
            'auth/reset_password.html',
            errors=errors,
            form=form,
            email=session['reset_email'],
            dev_code=session.get('reset_code'),
        )

    try:
        update_password(session['reset_user_id'], hash_password(form['mot_de_passe']))
    except mysql.connector.Error:
        flash('Impossible de réinitialiser le mot de passe pour le moment. Réessayez plus tard.', 'error')
        return render_template(
            'auth/reset_password.html',
            form=form,
            email=session['reset_email'],
            dev_code=session.get('reset_code'),
        )

    clear_reset_session()
    flash('Votre mot de passe a été réinitialisé. Vous pouvez vous connecter.', 'success')
    return redirect(url_for('auth.login'))

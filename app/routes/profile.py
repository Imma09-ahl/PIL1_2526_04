import os
import re

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.utils import secure_filename

from app.models.competences import (
    add_competence,
    delete_competence_for_user,
    get_competences,
)
from app.models.disponibilite import (
    JOURS_VALIDES,
    add_disponibilite,
    delete_disponibilite,
    get_disponibilites,
)
from app.models.user import (
    get_user_by_email,
    get_user_by_id,
    get_user_by_telephone,
    get_user_full_profile,
    update_user,
)
from app.utils.decorators import login_required

profile_bp = Blueprint('profile', __name__)

FILIERES = ['IA', 'IM', 'GL', 'SE&IoT', 'SI']
NIVEAUX = ['L1', 'L2', 'L3']
MATIERES_PREDEFINIES = [
    'Algorithme',
    'Python',
    'Java',
    'C/C++',
    'JavaScript',
    'Analyse combinatoire',
    'Équations différentielles',
    'Algèbre linéaire',
    'Probabilités et statistiques',
    'Base de données',
    'Réseaux informatiques',
    'Systèmes d\'exploitation',
    'Intelligence artificielle',
    'Machine Learning',
    'Développement web',
    'Développement mobile',
    'Génie logiciel',
    'Architecture logicielle',
    'Sécurité informatique',
    'Cloud computing',
]
EMAIL_PATTERN = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
TELEPHONE_PATTERN = re.compile(r'^(\+229|00229|229)?[0-9]{8,10}$')


def _allowed_file(filename):
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
    )


def _save_photo(file, user_id):
    if not file or not file.filename:
        return None
    if not _allowed_file(file.filename):
        return None

    filename = secure_filename(f'user_{user_id}_{file.filename}')
    upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    file.save(os.path.join(upload_dir, filename))
    return filename


def _validate_profile_form(form, user_id):
    errors = {}
    nom = (form.get('nom') or '').strip()
    prenom = (form.get('prenom') or '').strip()
    email = (form.get('email') or '').strip().lower()
    telephone = (form.get('telephone') or '').strip()
    filiere = (form.get('filiere') or '').strip()
    niveau = (form.get('niveau') or '').strip()
    bio = (form.get('bio') or '').strip()

    if not nom:
        errors['nom'] = 'Le nom est obligatoire.'
    if not prenom:
        errors['prenom'] = 'Le prénom est obligatoire.'
    if not email:
        errors['email'] = "L'adresse e-mail est obligatoire."
    elif not EMAIL_PATTERN.match(email):
        errors['email'] = "Le format de l'adresse e-mail est invalide."
    else:
        existing = get_user_by_email(email)
        if existing and existing['id'] != user_id:
            errors['email'] = 'Cette adresse e-mail est déjà utilisée.'

    if not telephone:
        errors['telephone'] = 'Le numéro de téléphone est obligatoire.'
    elif not TELEPHONE_PATTERN.match(telephone):
        errors['telephone'] = 'Le format du numéro de téléphone est invalide.'
    else:
        existing = get_user_by_telephone(telephone)
        if existing and existing['id'] != user_id:
            errors['telephone'] = 'Ce numéro de téléphone est déjà utilisé.'

    if filiere not in FILIERES:
        errors['filiere'] = 'Filière invalide.'
    if niveau not in NIVEAUX:
        errors['niveau'] = 'Niveau invalide.'
    if len(bio) > 500:
        errors['bio'] = 'La bio ne doit pas dépasser 500 caractères.'

    return errors, {
        'nom': nom,
        'prenom': prenom,
        'email': email,
        'telephone': telephone,
        'filiere': filiere,
        'niveau': niveau,
        'bio': bio,
    }


@profile_bp.route('/profile')
@login_required
def view_profile():
    user_id = session['user_id']
    profile = get_user_full_profile(user_id)

    if not profile:
        flash('Profil non trouvé.', 'error')
        return redirect(url_for('auth.login'))

    return render_template(
        'profile/view.html',
        profile=profile,
        is_own_profile=True,
    )


@profile_bp.route('/profile/<int:user_id>')
@login_required
def view_other_profile(user_id):
    profile = get_user_full_profile(user_id)

    if not profile:
        flash('Utilisateur non trouvé.', 'error')
        return redirect(url_for('profile.view_profile'))

    is_own = user_id == session.get('user_id')
    return render_template(
        'profile/view.html',
        profile=profile,
        is_own_profile=is_own,
    )


@profile_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user_id = session['user_id']
    user = get_user_by_id(user_id)

    if not user:
        flash('Utilisateur non trouvé.', 'error')
        return redirect(url_for('auth.login'))

    competences = get_competences(user_id)
    forces = [c for c in competences if c['type'] == 'fort']
    faiblesses = [c for c in competences if c['type'] == 'faible']
    disponibilites = get_disponibilites(user_id)

    if request.method == 'POST':
        errors, form_data = _validate_profile_form(request.form, user_id)

        if errors:
            return render_template(
                'profile/edit.html',
                user={**user, **form_data},
                forces=forces,
                faiblesses=faiblesses,
                disponibilites=disponibilites,
                filieres=FILIERES,
                niveaux=NIVEAUX,
                jours=JOURS_VALIDES,
                errors=errors,
            )

        photo = user.get('photo') or ''
        uploaded = _save_photo(request.files.get('photo_file'), user_id)
        if uploaded:
            photo = uploaded
        elif request.form.get('photo'):
            photo = request.form.get('photo').strip()

        update_user(
            user_id,
            form_data['nom'],
            form_data['prenom'],
            form_data['email'],
            form_data['telephone'],
            form_data['filiere'],
            form_data['niveau'],
            form_data['bio'],
            photo,
        )

        session['user_nom'] = form_data['nom']
        session['user_prenom'] = form_data['prenom']
        session['user_email'] = form_data['email']

        flash('Profil mis à jour avec succès.', 'success')
        return redirect(url_for('profile.view_profile'))

    return render_template(
        'profile/edit.html',
        user=user,
        forces=forces,
        faiblesses=faiblesses,
        disponibilites=disponibilites,
        filieres=FILIERES,
        niveaux=NIVEAUX,
        jours=JOURS_VALIDES,
        matieres_predefinies=MATIERES_PREDEFINIES,
        errors={},
    )


@profile_bp.route('/profile/competence/add', methods=['POST'])
@login_required
def add_user_competence():
    user_id = session['user_id']
    matiere = (request.form.get('matiere') or '').strip()
    type_comp = (request.form.get('type') or '').strip()

    if not matiere:
        flash('Veuillez saisir le nom de la matière.', 'error')
    elif type_comp not in ('fort', 'faible'):
        flash('Type de compétence invalide.', 'error')
    elif len(matiere) > 100:
        flash('Le nom de la matière ne doit pas dépasser 100 caractères.', 'error')
    else:
        add_competence(user_id, matiere, type_comp)
        flash(f'Matière « {matiere} » ajoutée.', 'success')

    return redirect(url_for('profile.edit_profile'))


@profile_bp.route('/profile/competence/delete/<int:competence_id>', methods=['POST'])
@login_required
def delete_user_competence(competence_id):
    delete_competence_for_user(competence_id, session['user_id'])
    flash('Compétence supprimée.', 'success')
    return redirect(url_for('profile.edit_profile'))


@profile_bp.route('/profile/disponibilite/add', methods=['POST'])
@login_required
def add_user_disponibilite():
    user_id = session['user_id']
    jour = (request.form.get('jour') or '').strip()
    heure_debut = (request.form.get('heure_debut') or '').strip()
    heure_fin = (request.form.get('heure_fin') or '').strip()

    if jour not in JOURS_VALIDES:
        flash('Jour invalide.', 'error')
    elif not heure_debut or not heure_fin:
        flash('Veuillez renseigner les heures de début et de fin.', 'error')
    elif heure_debut >= heure_fin:
        flash("L'heure de fin doit être après l'heure de début.", 'error')
    else:
        add_disponibilite(user_id, jour, heure_debut, heure_fin)
        flash('Créneau ajouté.', 'success')

    return redirect(url_for('profile.edit_profile'))


@profile_bp.route('/profile/disponibilite/delete/<int:disponibilite_id>', methods=['POST'])
@login_required
def delete_user_disponibilite(disponibilite_id):
    delete_disponibilite(disponibilite_id, session['user_id'])
    flash('Créneau supprimé.', 'success')
    return redirect(url_for('profile.edit_profile'))

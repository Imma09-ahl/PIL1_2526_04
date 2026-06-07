from flask import Blueprint, render_template, request, redirect, url_for, flash

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/profile')
def view_profile():
    """Affiche le profil de l'utilisateur connecté"""
    # TEMPORAIRE: sans auth, on passe user_id en paramètre
    # Exemple: /profile?user_id=1
    user_id = request.args.get('user_id', 1)
    
    from app.models.user import get_user_full_profile
    profile = get_user_full_profile(user_id)
    
    if not profile:
        flash("Profil non trouvé", "error")
        return redirect(url_for('profile.view_profile'))
    
    # TEMPORAIRE: toujours "son propre profil" pour tester
    is_own_profile = True
    
    return render_template('profile/view.html', 
                         profile=profile, 
                         is_own_profile=is_own_profile)


@profile_bp.route('/profile/<int:user_id>')
def view_other_profile(user_id):
    """Voir le profil d'un autre utilisateur (pour le matching)"""
    from app.models.user import get_user_full_profile
    profile = get_user_full_profile(user_id)
    
    if not profile:
        flash("Utilisateur non trouvé", "error")
        return redirect(url_for('profile.view_profile'))
    
    return render_template('profile/view.html', 
                         profile=profile, 
                         is_own_profile=False)


@profile_bp.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    """Modifier son profil"""
    # TEMPORAIRE: sans auth
    user_id = request.args.get('user_id', 1)
    
    from app.models.user import get_user_by_id, update_user
    from app.models.competences import get_competences
    
    user = get_user_by_id(user_id)
    if not user:
        flash("Utilisateur non trouvé", "error")
        return redirect(url_for('profile.view_profile'))
    
    if request.method == 'POST':
        # Récupère les données du formulaire
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        email = request.form.get('email')
        telephone = request.form.get('telephone')
        filiere = request.form.get('filiere')
        niveau = request.form.get('niveau')
        bio = request.form.get('bio')
        photo = request.form.get('photo', '')
        
        # Met à jour en base
        update_user(user_id, nom, prenom, email, telephone, 
                   filiere, niveau, bio, photo)
        
        flash("Profil mis à jour avec succès", "success")
        return redirect(url_for('profile.view_profile', user_id=user_id))
    
    # GET: affiche le formulaire pré-rempli
    competences = get_competences(user_id)
    forces = [c for c in competences if c['type'] == 'fort']
    faiblesses = [c for c in competences if c['type'] == 'faible']
    
    return render_template('profile/edit.html',
                         user=user,
                         forces=forces,
                         faiblesses=faiblesses,
                         filieres=['IA', 'IM', 'GL', 'SE&IoT', 'SI'],
                         niveaux=['L1', 'L2', 'L3'])


@profile_bp.route('/profile/competence/add', methods=['POST'])
def add_user_competence():
    """Ajouter une compétence (force ou faiblesse)"""
    user_id = request.form.get('user_id', 1)
    matiere = request.form.get('matiere')
    type_comp = request.form.get('type')  # 'fort' ou 'faible'
    
    if matiere and type_comp in ['fort', 'faible']:
        from app.models.competences import add_competence
        add_competence(user_id, matiere, type_comp)
        flash("Compétence ajoutée", "success")
    
    return redirect(url_for('profile.edit_profile', user_id=user_id))


@profile_bp.route('/profile/competence/delete/<int:competence_id>')
def delete_user_competence(competence_id):
    """Supprimer une compétence"""
    from app.models.competences import delete_competence
    delete_competence(competence_id)
    flash("Compétence supprimée", "success")
    
    user_id = request.args.get('user_id', 1)
    return redirect(url_for('profile.edit_profile', user_id=user_id))
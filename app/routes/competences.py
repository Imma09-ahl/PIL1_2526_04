from datetime import timedelta

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.models.competences import (
    add_competence,
    delete_competence_utilisateur,
    get_competences,
)
from app.models.disponibilite import (
    add_disponibilite,
    delete_disponibilite,
    get_disponibilites,
)

competences_bp = Blueprint('competences', __name__)

# En attendant le module auth (ne pas modifier les autres branches)
TEST_USER_ID = 1

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
        return f"{hours:02d}:{minutes:02d}"
    if hasattr(value, 'strftime'):
        return value.strftime('%H:%M')
    return str(value)[:5]


def _filtrer_competences(competences, q, type_filtre):
    result = competences
    if q:
        result = [c for c in result if q in c['matiere'].lower()]
    if type_filtre in ('fort', 'faible'):
        result = [c for c in result if c['type'] == type_filtre]
    return result


@competences_bp.route('/competences')
def index():
    user_id = TEST_USER_ID
    q = request.args.get('q', '').strip().lower()
    type_filtre = request.args.get('type', '').strip()

    toutes = get_competences(user_id)
    filtrees = _filtrer_competences(toutes, q, type_filtre)

    fortes = [c for c in filtrees if c['type'] == 'fort']
    faibles = [c for c in filtrees if c['type'] == 'faible']

    dispos = []
    for d in get_disponibilites(user_id):
        dispos.append({
            **d,
            'heure_debut_fmt': _format_heure(d['heure_debut']),
            'heure_fin_fmt': _format_heure(d['heure_fin']),
        })

    return render_template(
        'competences/list.html',
        fortes=fortes,
        faibles=faibles,
        disponibilites=dispos,
        filtre_q=request.args.get('q', ''),
        filtre_type=type_filtre,
        jours=JOURS_VALIDES,
    )


@competences_bp.route('/competences/ajouter', methods=['POST'])
def ajouter():
    user_id = TEST_USER_ID
    matiere = request.form.get('matiere', '').strip()
    type_comp = request.form.get('type', '').strip()

    if not matiere:
        flash('Veuillez saisir le nom de la matière.', 'error')
        return redirect(url_for('competences.index'))

    if type_comp not in ('fort', 'faible'):
        flash('Type invalide : choisissez matière forte ou faible.', 'error')
        return redirect(url_for('competences.index'))

    if len(matiere) > 100:
        flash('Le nom de la matière ne doit pas dépasser 100 caractères.', 'error')
        return redirect(url_for('competences.index'))

    add_competence(user_id, matiere, type_comp)
    flash(f'Matière « {matiere} » ajoutée.', 'success')
    return redirect(url_for('competences.index'))


@competences_bp.route('/competences/supprimer', methods=['POST'])
def supprimer():
    user_id = TEST_USER_ID
    competence_id = request.form.get('competence_id', type=int)

    if not competence_id:
        flash('Identifiant de matière manquant.', 'error')
        return redirect(url_for('competences.index'))

    delete_competence_utilisateur(competence_id, user_id)
    flash('Matière supprimée.', 'success')
    return redirect(url_for('competences.index'))


@competences_bp.route('/competences/disponibilite/ajouter', methods=['POST'])
def ajouter_disponibilite():
    user_id = TEST_USER_ID
    jour = request.form.get('jour', '').strip()
    heure_debut = request.form.get('heure_debut', '').strip()
    heure_fin = request.form.get('heure_fin', '').strip()

    if jour not in JOURS_VALIDES:
        flash('Jour invalide.', 'error')
        return redirect(url_for('competences.index'))

    if not heure_debut or not heure_fin:
        flash('Veuillez renseigner les heures de début et de fin.', 'error')
        return redirect(url_for('competences.index'))

    if heure_debut >= heure_fin:
        flash("L'heure de fin doit être après l'heure de début.", 'error')
        return redirect(url_for('competences.index'))

    add_disponibilite(user_id, jour, heure_debut, heure_fin)
    flash('Créneau ajouté.', 'success')
    return redirect(url_for('competences.index'))


@competences_bp.route('/competences/disponibilite/supprimer', methods=['POST'])
def supprimer_disponibilite():
    user_id = TEST_USER_ID
    disponibilite_id = request.form.get('disponibilite_id', type=int)

    if not disponibilite_id:
        flash('Identifiant de créneau manquant.', 'error')
        return redirect(url_for('competences.index'))

    delete_disponibilite(disponibilite_id, user_id)
    flash('Créneau supprimé.', 'success')
    return redirect(url_for('competences.index'))

from datetime import timedelta

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.models.competences import (
    add_competence,
    delete_competence_for_user,
    get_competences,
)
from app.models.disponibilite import (
    add_disponibilite,
    delete_disponibilite,
    get_disponibilites,
)
from app.models.user import get_user_by_id, update_format_mentorat
from app.utils.decorators import login_required

competences_bp = Blueprint('competences', __name__)

JOURS_VALIDES = (
    'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'
)
FORMATS_VALIDES = ('presentiel', 'enligne', 'les_deux')


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


def _filtrer_competences(competences, q, type_filtre):
    result = competences
    if q:
        result = [c for c in result if q in c['matiere'].lower()]
    if type_filtre in ('fort', 'faible'):
        result = [c for c in result if c['type'] == type_filtre]
    return result


@competences_bp.route('/competences')
@login_required
def index():
    user_id = session['user_id']
    user = get_user_by_id(user_id)
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

    format_actuel = (user or {}).get('format_mentorat') or 'les_deux'

    return render_template(
        'competences/list.html',
        fortes=fortes,
        faibles=faibles,
        disponibilites=dispos,
        filtre_q=request.args.get('q', ''),
        filtre_type=type_filtre,
        jours=JOURS_VALIDES,
        format_actuel=format_actuel,
    )


@competences_bp.route('/competences/ajouter', methods=['POST'])
@login_required
def ajouter():
    user_id = session['user_id']
    matiere = request.form.get('matiere', '').strip()
    type_comp = request.form.get('type', '').strip()

    if not matiere:
        flash('Veuillez saisir le nom de la matière.', 'error')
    elif type_comp not in ('fort', 'faible'):
        flash('Type invalide : choisissez matière forte ou faible.', 'error')
    elif len(matiere) > 100:
        flash('Le nom de la matière ne doit pas dépasser 100 caractères.', 'error')
    else:
        add_competence(user_id, matiere, type_comp)
        flash(f'Matière « {matiere} » ajoutée.', 'success')

    return redirect(url_for('competences.index'))


@competences_bp.route('/competences/supprimer', methods=['POST'])
@login_required
def supprimer():
    user_id = session['user_id']
    competence_id = request.form.get('competence_id', type=int)

    if not competence_id:
        flash('Identifiant de matière manquant.', 'error')
    else:
        delete_competence_for_user(competence_id, user_id)
        flash('Matière supprimée.', 'success')

    return redirect(url_for('competences.index'))


@competences_bp.route('/competences/disponibilite/ajouter', methods=['POST'])
@login_required
def ajouter_disponibilite():
    user_id = session['user_id']
    jour = request.form.get('jour', '').strip()
    heure_debut = request.form.get('heure_debut', '').strip()
    heure_fin = request.form.get('heure_fin', '').strip()

    if jour not in JOURS_VALIDES:
        flash('Jour invalide.', 'error')
    elif not heure_debut or not heure_fin:
        flash('Veuillez renseigner les heures de début et de fin.', 'error')
    elif heure_debut >= heure_fin:
        flash("L'heure de fin doit être après l'heure de début.", 'error')
    else:
        add_disponibilite(user_id, jour, heure_debut, heure_fin)
        flash('Créneau ajouté.', 'success')

    return redirect(url_for('competences.index'))


@competences_bp.route('/competences/disponibilite/supprimer', methods=['POST'])
@login_required
def supprimer_disponibilite():
    user_id = session['user_id']
    disponibilite_id = request.form.get('disponibilite_id', type=int)

    if not disponibilite_id:
        flash('Identifiant de créneau manquant.', 'error')
    else:
        delete_disponibilite(disponibilite_id, user_id)
        flash('Créneau supprimé.', 'success')

    return redirect(url_for('competences.index'))


@competences_bp.route('/competences/format', methods=['POST'])
@login_required
def sauvegarder_format():
    format_mentorat = request.form.get('format', '').strip()

    if format_mentorat not in FORMATS_VALIDES:
        flash('Format de séance invalide.', 'error')
    else:
        update_format_mentorat(session['user_id'], format_mentorat)
        flash('Format de séance enregistré.', 'success')

    return redirect(url_for('competences.index'))

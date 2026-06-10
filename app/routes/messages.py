from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, session, url_for

from app.models.message import (
    find_or_create_conversation,
    get_conversation,
    get_conversations,
    get_messages,
    get_new_messages,
    send_message,
    user_in_conversation,
)
from app.utils.decorators import login_required

messages_bp = Blueprint('messages', __name__)


def _other_participant(conversation, user_id):
    if conversation['utilisateur1_id'] == user_id:
        return {
            'prenom': conversation['prenom2'],
            'nom': conversation['nom2'],
        }
    return {
        'prenom': conversation['prenom1'],
        'nom': conversation['nom1'],
    }


@messages_bp.route('/messages')
@login_required
def index():
    conversations = get_conversations(session['user_id'])
    return render_template(
        'messages/index.html',
        conversations=conversations,
    )


@messages_bp.route('/messages/<int:conversation_id>', methods=['GET', 'POST'])
@login_required
def conversation(conversation_id):
    user_id = session['user_id']

    if not user_in_conversation(conversation_id, user_id):
        flash("Vous n'avez pas accès à cette conversation.", 'error')
        return redirect(url_for('messages.index'))

    conv = get_conversation(conversation_id)
    other = _other_participant(conv, user_id)

    if request.method == 'POST':
        contenu = (request.form.get('contenu') or '').strip()
        if not contenu:
            flash('Le message ne peut pas être vide.', 'error')
        elif len(contenu) > 2000:
            flash('Le message ne doit pas dépasser 2000 caractères.', 'error')
        else:
            send_message(conversation_id, user_id, contenu)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                messages = get_messages(conversation_id)
                last = messages[-1] if messages else None
                return jsonify({
                    'id': last['id'],
                    'contenu': last['contenu'],
                    'prenom': last['prenom'],
                    'nom': last['nom'],
                    'expediteur_id': last['expediteur_id'],
                    'created_at': str(last['created_at']),
                })
            return redirect(url_for('messages.conversation', conversation_id=conversation_id))

    messages = get_messages(conversation_id)
    return render_template(
        'messages/conversation.html',
        messages=messages,
        conversation_id=conversation_id,
        other=other,
    )


@messages_bp.route('/messages/<int:conversation_id>/nouveaux')
@login_required
def nouveaux_messages(conversation_id):
    if not user_in_conversation(conversation_id, session['user_id']):
        abort(403)

    last_id = request.args.get('last_id', 0, type=int)
    messages = get_new_messages(conversation_id, last_id)

    return jsonify({
        'messages': [
            {
                'id': m['id'],
                'contenu': m['contenu'],
                'prenom': m['prenom'],
                'nom': m['nom'],
                'expediteur_id': m['expediteur_id'],
                'created_at': str(m['created_at']),
            }
            for m in messages
            if m['expediteur_id'] != session['user_id']
        ],
    })


@messages_bp.route('/messages/nouvelle/<int:autre_utilisateur_id>', methods=['POST'])
@login_required
def nouvelle_conversation(autre_utilisateur_id):
    conversation_id = find_or_create_conversation(session['user_id'], autre_utilisateur_id)

    if not conversation_id:
        flash('Impossible de créer cette conversation.', 'error')
        return redirect(url_for('messages.index'))

    return redirect(url_for('messages.conversation', conversation_id=conversation_id))

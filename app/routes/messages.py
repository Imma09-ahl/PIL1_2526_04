from flask import Blueprint, flash, redirect, session, url_for

from app.models.message import find_or_create_conversation
from app.utils.decorators import login_required

messages_bp = Blueprint('messages', __name__)


@messages_bp.route('/messages')
@login_required
def index():
    flash('Module messagerie complet disponible après fusion de feature/messagerie.', 'success')
    return redirect(url_for('matching.resultats'))


@messages_bp.route('/messages/<int:conversation_id>')
@login_required
def conversation(conversation_id):
    flash('Conversation accessible après fusion de feature/messagerie.', 'success')
    return redirect(url_for('matching.resultats'))


@messages_bp.route('/messages/nouvelle/<int:autre_utilisateur_id>', methods=['POST'])
@login_required
def nouvelle_conversation(autre_utilisateur_id):
    conversation_id = find_or_create_conversation(session['user_id'], autre_utilisateur_id)
    if not conversation_id:
        flash('Impossible de créer cette conversation.', 'error')
        return redirect(url_for('matching.resultats'))
    flash('Conversation créée. La messagerie complète sera disponible après fusion.', 'success')
    return redirect(url_for('matching.resultats'))

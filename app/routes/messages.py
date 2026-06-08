from flask import Blueprint, request, session, jsonify, render_template, redirect, url_for
from app.models.message import create_conversation, send_message, get_messages, get_conversations

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/messages')
def index():
    if 'user_id' not in session:
        pass
    conversations = []
    return render_template('messages/index.html', conversations=conversations)

@messages_bp.route('/messages/<int:conversation_id>', methods=['GET', 'POST'])
def conversation(conversation_id):
    if 'user_id' not in session:
        pass
    if request.method == 'POST':
        contenu = request.form.get('contenu')
        if contenu:
            send_message(conversation_id, session['user_id'], contenu)
    messages = get_messages(conversation_id)
    return render_template('messages/conversation.html', messages=messages, conversation_id=conversation_id)

@messages_bp.route('/messages/nouvelle/<int:autre_utilisateur_id>', methods=['POST'])
def nouvelle_conversation(autre_utilisateur_id):
    if 'user_id' not in session:
        pass
    conversation_id = create_conversation(session['user_id'], autre_utilisateur_id)
    return redirect(url_for('messages.conversation', conversation_id=conversation_id))

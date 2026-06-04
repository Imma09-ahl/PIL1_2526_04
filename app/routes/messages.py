from flask import Blueprint

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/messages')
def index():
    pass

@messages_bp.route('/messages/<int:conversation_id>')
def conversation(conversation_id):
    pass
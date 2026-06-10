from flask import Flask
from flask_session import Session
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configuration de Flask-Session
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    Session(app)

    from .routes.auth import auth_bp
    from .routes.profile import profile_bp
    from .routes.competences import competences_bp
    from .routes.matching import matching_bp
    from .routes.messages import messages_bp
    from .routes.dashboard import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(competences_bp)
    app.register_blueprint(matching_bp)
    app.register_blueprint(messages_bp)
    app.register_blueprint(dashboard_bp)

    return app
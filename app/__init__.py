from flask import Flask
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from .routes.auth import auth_bp
    from .routes.dashboard import dashboard_bp
    from .routes.profile import profile_bp
    from .routes.matching import matching_bp
    from .routes.messages import messages_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(matching_bp)
    app.register_blueprint(messages_bp)

    return app
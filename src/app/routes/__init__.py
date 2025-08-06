
from flask import Flask
from flask_cors import CORS
from app.routes.config_routes import config_bp
from app.routes.policy_routes import policy_bp

def create_flask_app():
    app = Flask(__name__)
    app.register_blueprint(config_bp,url_prefix="/config")
    app.register_blueprint(policy_bp,url_prefix="/policy")
    CORS(app)
    return app
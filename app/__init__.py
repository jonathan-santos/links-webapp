from flask_login import LoginManager
from flask import Flask

from .config import load_config
from .routes import create_routes
from .auth import config_auth

login_manager = LoginManager()

def init_app():
  app = Flask(__name__)

  load_config(app)

  login_manager.init_app(app)

  with app.app_context():
    create_routes(app)
    config_auth(login_manager)

    return app

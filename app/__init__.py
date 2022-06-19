from flask_login import LoginManager
from flask import Flask

from .config import load_config
from .auth import config_auth

from .index.router import index

login_manager = LoginManager()

def init_app():
  app = Flask(__name__)

  load_config(app)

  login_manager.init_app(app)

  with app.app_context():
    # from .index import routes

    # Register Blueprints
    app.register_blueprint(index)

    config_auth(login_manager)

    return app

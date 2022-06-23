from flask import Flask
from flask_login import LoginManager

from .config import load_config
from .auth import config_auth

from .routes import routes

login_manager = LoginManager()

def init_app():
  app = Flask(__name__)

  load_config(app)
  login_manager.init_app(app)

  with app.app_context():
    for route in routes:
      app.register_blueprint(route)

    config_auth(login_manager)

    return app

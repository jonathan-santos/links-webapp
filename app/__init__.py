from flask_login import LoginManager
from flask import Flask

from .config import load_config
from .auth import config_auth

from .index.router import index
from .register.router import register
from .login.router import login

login_manager = LoginManager()

def init_app():
  app = Flask(__name__)

  load_config(app)
  login_manager.init_app(app)

  with app.app_context():
    app.register_blueprint(index)
    app.register_blueprint(register)
    app.register_blueprint(login)

    config_auth(login_manager)

    return app

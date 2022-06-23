from flask import Flask
from flask_login import LoginManager

from .config import load_config
from .auth import config_auth

from .routes.index.router import index
from .routes.register.router import register
from .routes.login.router import login
from .routes.logout.router import logout
from .routes.links_new.router import links_new
from .routes.user_links.router import user_links
from .routes.tag.router import tag
from .routes.tags.router import tags
from .routes.tags_new.router import tags_new

login_manager = LoginManager()

def init_app():
  app = Flask(__name__)

  load_config(app)
  login_manager.init_app(app)

  with app.app_context():
    app.register_blueprint(index)
    app.register_blueprint(register)
    app.register_blueprint(login)
    app.register_blueprint(logout)
    app.register_blueprint(links_new)
    app.register_blueprint(user_links)
    app.register_blueprint(tag)
    app.register_blueprint(tags)
    app.register_blueprint(tags_new)

    config_auth(login_manager)

    return app

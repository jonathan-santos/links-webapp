from http import HTTPStatus
from flask_login import LoginManager
from flask import Flask, redirect, request, abort

from .config import load_config
from .db import get_db_connection
from .models import User
from .routes import create_routes

login_manager = LoginManager()

def create_app():
  app = Flask(__name__)

  load_config(app)

  login_manager.init_app(app)

  with app.app_context():
    create_routes(app)

    @login_manager.unauthorized_handler
    def unauthorized():
      if request.blueprint == 'api':
          abort(HTTPStatus.UNAUTHORIZED)

      return redirect('/login')

    @login_manager.user_loader
    def load_user(user_id):
      con = get_db_connection()
      cur = con.cursor()

      cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
      user = cur.fetchone()

      if not user:
        return None

      return User(user[0], user[1], user[2])

    return app

from http import HTTPStatus
from flask import redirect, request, abort

from .db import get_db_connection
from .models import User

def config_auth(login_manager):
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
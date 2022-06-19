from flask import redirect, request, abort
from flask_login import login_user, current_user
from http import HTTPStatus

from .db import DB

class User ():
  def __init__(self, id, username, email):
    self.id = id
    self.username = username
    self.email = email
    self.is_authenticated = True
    self.is_active = True
    self.is_anonymous = False

  def get_id(self):
    return str(self.id)

def user_login(user_id, username, email):
  login_user(User(user_id, username, email))

def is_user_authenticated():
  return current_user.is_authenticated

def config_auth(login_manager):
  @login_manager.unauthorized_handler
  def unauthorized():
    if request.blueprint == 'api':
        abort(HTTPStatus.UNAUTHORIZED)

    return redirect('/login')

  @login_manager.user_loader
  def load_user(user_id):
    db = DB("SELECT id, username, email FROM users WHERE id = %s", [user_id])
    user = db.getOne()
    db.close()

    if not user:
      return None

    return User(id=user[0], username=user[1], email=user[2])

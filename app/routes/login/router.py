from flask import Blueprint, redirect, render_template, request
from re import match
from werkzeug.security import check_password_hash

from app.db import DB
from app.auth import is_user_authenticated, user_login

login = Blueprint(
  'login', __name__,
  template_folder='templates'
)

@login.route('/login', methods=['GET', 'POST'])
def login_page():
  if is_user_authenticated():
    return redirect('/')
  
  if (request.method == 'GET'):
    return render_template('login.html')
  
  email = request.form.get('email', '')
  password = request.form.get('password', '')

  if not email:
      return ("email cannot be empty", 400)

  if not match('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email):
    return ("email is invalid", 400)

  if len(email) > 50:
    return ("email length cannot be greater than 255", 400)

  if not password:
    return ("password cannot be empty", 400)

  if len(password) < 2:
    return ("password length cannot be lower than 2", 400)

  if len(password) > 50:
    return ("password length cannot be greater than 50", 400)

  db = DB("SELECT * FROM users WHERE email = %s", [email])
  user = db.getOne()
  db.close()

  if not user:
    return ("email not found", 400)

  if not check_password_hash(user[3], password):
    return ("wrong password", 400)

  user_login(user)

  return redirect('/')

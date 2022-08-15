from flask import Blueprint, redirect, render_template, request
from flask_login import login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from re import match

from app.db import DB
from app.auth import is_user_authenticated, user_login

auth = Blueprint(
  'auth', __name__,
  template_folder='templates'
)

@auth.route('/logout/')
@login_required
def logout_page():
  logout_user()
  return redirect('/')

@auth.route('/signup/', methods=['GET', 'POST'])
def signup_page():
  if is_user_authenticated():
    return redirect('/')

  if (request.method == 'GET'):
    return render_template('signup.html')
  
  username = request.form.get('username', '')
  email = request.form.get('email', '')
  password = request.form.get('password', '')

  if not username:
      return ("username cannot be empty", 400)

  if len(username) < 2:
    return ("username length cannot be lower than 2", 400)

  if len(username) > 50:
    return ("username length cannot be greater than 50", 400)

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

  db = DB("SELECT id FROM users WHERE username = %s", [username])

  username_already_exists = db.getOne()

  if (username_already_exists):
    db.close()
    return ("username already used", 400)

  db.execute("SELECT id FROM users WHERE email = %s", [email])
  
  email_already_exists = db.getOne()

  if (email_already_exists):
    db.close()
    return ("email already used", 400)

  password_hash = generate_password_hash(password)

  db.execute("""
    INSERT INTO users (username, email, password, created_at)
    VALUES (%s, %s, %s, NOW())
    RETURNING id
  """, [username, email, password_hash])

  user_id = db.getOne()[0]

  user = {
    "id": user_id,
    "username": username,
    "email": email,
    "password": password_hash
  }

  user_login(user)

  db.save()
  db.close()

  return redirect('/')


@auth.route('/login/', methods=['GET', 'POST'])
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

  if not check_password_hash(user["password"], password):
    return ("wrong password", 400)

  user_login(user)

  return redirect('/')

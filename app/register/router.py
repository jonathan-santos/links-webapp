from re import match
from flask import Blueprint, redirect, render_template, request
from werkzeug.security import generate_password_hash

from ..db import DB
from ..auth import is_user_authenticated, user_login

register = Blueprint(
  'register', __name__,
  template_folder='templates'
)

@register.route('/register', methods=['GET', 'POST'])
def register_page():
  if is_user_authenticated():
    return redirect('/')

  if (request.method == 'GET'):
    return render_template('register.html')
  
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
    "email": email
  }

  user_login(user)

  db.save()
  db.close()

  return redirect('/')

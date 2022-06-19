from flask import Blueprint, redirect, render_template, request
from werkzeug.security import generate_password_hash

from ..db import get_db_connection
from ..auth import is_user_authenticated, user_login

register = Blueprint(
  'register', __name__,
  template_folder='templates'
)

@register.route('/register', methods=['GET', 'POST'])
def register_page():
  # if is_user_authenticated:
  #   return redirect('/')
  
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

  if not re.match('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email):
    return ("email is invalid", 400)

  if len(email) > 50:
    return ("email length cannot be greater than 255", 400)

  if not password:
    return ("password cannot be empty", 400)

  if len(password) < 2:
    return ("password length cannot be lower than 2", 400)

  if len(password) > 50:
    return ("password length cannot be greater than 50", 400)

  con = get_db_connection()
  cur = con.cursor()

  cur.execute("SELECT username FROM users")
  same_usernames = cur.fetchone() or []

  if (not len(same_usernames) == 0):
    cur.close()
    con.close()
    return ("username already used", 400)

  cur.execute("SELECT email FROM users")
  same_emails = cur.fetchone() or []

  if (not len(same_emails) == 0):
    cur.close()
    con.close()
    return ("email already used", 400)

  password_hash = generate_password_hash(password)

  cur.execute("""
    INSERT INTO users (username, email, password, created_at)
    VALUES (%s, %s, %s, NOW())
    RETURNING id
  """, (username, email, password_hash))

  user_id = cur.fetchone()[0]

  user_login(user_id, username, email)

  con.commit()
  cur.close()
  con.close()

  return redirect('/')

import re

from .db import get_db_connection
from .models import User

from flask_login import login_required, login_user, logout_user, current_user
from flask import redirect, render_template, request
from werkzeug.security import check_password_hash

def create_routes(app):
  @app.route('/logout')
  @login_required
  def logout():
    logout_user()
    return redirect('/')

  @app.route('/login', methods=['GET', 'POST'])
  def login():
    if current_user.is_authenticated:
      return redirect('/')
    
    if (request.method == 'GET'):
      return render_template('login.html')
    
    email = request.form.get('email', '')
    password = request.form.get('password', '')

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

    cur.execute("SELECT * FROM users WHERE email =  %s", (email,))
    user = cur.fetchone()

    if not user:
      return ("email not found", 400)

    if not check_password_hash(user[3], password):
      return ("wrong password", 400)

    login_user(User(user[0], user[1], user[2]))

    cur.close()
    con.close()
    return redirect('/')

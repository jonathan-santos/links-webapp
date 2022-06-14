import re
import os
import sys

from .db import get_db_connection
from .models import User

from http import HTTPStatus
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for, abort
from werkzeug.security import check_password_hash, generate_password_hash

def create_app():
  app = Flask(__name__) 

  if not os.path.isfile(".env"):
    print("\nNo '.env' file found! Exiting...\n")
    sys.exit(4)

  load_dotenv()

  app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

  login_manager = LoginManager()
  login_manager.init_app(app)

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

  @app.route('/')
  def index():
    return render_template('index.html')

  @app.route('/logout')
  @login_required
  def logout():
    logout_user()
    return redirect('/')

  @app.route('/register', methods=['GET', 'POST'])
  def register():
    if current_user.is_authenticated:
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

    login_user(User(user_id, username, email))

    con.commit()
    cur.close()
    con.close()

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

  return app
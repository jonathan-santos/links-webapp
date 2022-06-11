import psycopg2
import re
import os
import sys

from flask_login import LoginManager
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for

def get_db_connection():
    conn = psycopg2.connect(
      dbname=os.environ['DB_DATABASE'],
      user=os.environ['DB_USER'],
      password=os.environ['DB_PASSWORD'],
      host=os.environ['DB_HOST']
    )

    return conn

def create_app():
  app = Flask(__name__) 

  if not os.path.isfile(".env"):
    print("\nNo '.env' file found! Exiting...\n")
    sys.exit(4)

  load_dotenv()

  login_manager = LoginManager()
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(user_id):
    return None #User.get(user_id)

  @app.route('/')
  def index():
    return render_template('index.html')

  @app.route('/register', methods=['GET', 'POST'])
  def register():
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

    return ('OK', 200)

  @app.route('/login', methods=['GET', 'POST'])
  def login():
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

    return ('OK', 200)

  return app
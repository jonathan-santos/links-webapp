import psycopg2
import os
import sys

from dotenv import load_dotenv
from flask import Flask, render_template

def create_app():
  app = Flask(__name__) 

  if not os.path.isfile(".env"):
    print("\nNo '.env' file found! Exiting...\n")
    sys.exit(4)

  load_dotenv()

  @app.route('/something')
  def something():
    conn = psycopg2.connect(dbname=os.environ['DB_DATABASE'], user=os.environ['DB_USER'], password=os.environ['DB_PASSWORD'], host=os.environ['DB_HOST'])

    cur = conn.cursor()

    cur.execute("SELECT * FROM links")

    print(cur.fetchall())

    cur.close()

    conn.close()
    
    return 'OK', 200

  @app.route('/')
  def index():
    return render_template('index.html')

  @app.route('/register')
  def register():
    return render_template('register.html')

  @app.route('/login')
  def login():
    return render_template('login.html')

  return app
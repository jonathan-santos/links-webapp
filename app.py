import psycopg2
import os
import sys

from dotenv import load_dotenv
from flask import Flask, render_template

app = Flask(__name__)

if not os.path.isfile(".env"):
  print("No '.env' file found! Exiting...")
  sys.exit(1)

load_dotenv()

@app.route('/something')
def something():
  conn = psycopg2.connect(dbname=os.environ['DB_DATABASE'], user=os.environ['DB_USER'], password=os.environ['DB_PASSWORD'], host=os.environ['DB_HOST'])

  cur = conn.cursor()

  cur.close()

  conn.close()
  
  return 'OK', 200

@app.route('/')
def home():
  return render_template('home.html')

if __name__ == "__main__":
  app.run(debug=True)
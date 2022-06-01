from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

@app.route('/init')
def init():
  conn = psycopg2.connect(dbname="links-app_db", user="postgres", password="postgres", host="postgres")

  cur = conn.cursor()

  cur.execute("CREATE TABLE something (name TEXT)")

  conn.commit()
  
  return 'OK', 200

@app.route('/')
def home():
  return render_template('home.html')

if __name__ == "__main__":
  app.run(debug=True)
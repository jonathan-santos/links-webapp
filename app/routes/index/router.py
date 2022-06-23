from flask import Blueprint, render_template
from flask_login import login_required

from ...db import DB

index = Blueprint(
  'index', __name__,
  template_folder='templates'
)

@login_required
@index.route('/')
def index_page():
  db = DB("SELECT url FROM links ORDER BY random() LIMIT 1")
  link = db.getOne()[0]
  db.close()

  return render_template('index.html', link=link)
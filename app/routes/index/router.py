from flask import Blueprint, render_template
from flask_login import login_required

from app.db import DB

index = Blueprint(
  'index', __name__,
  template_folder='templates'
)

@index.route('/')
def index_page():
  db = DB("""
    SELECT links.url, tags.id AS tag_id, tags.tagname
      FROM links
      JOIN tags
        ON links.tag_id = tags.id
  ORDER BY random()
     LIMIT 1
  """)
  link = db.getOne()

  db.close()

  return render_template('index.html', link=link)
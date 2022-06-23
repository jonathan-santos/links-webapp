from flask import Blueprint, render_template

from ...db import DB

tags = Blueprint(
  'tags', __name__,
  template_folder='templates'
)

@tags.route('/tags')
def tags_page():
  db = DB("SELECT title from tags")
  tags = db.getAll()
  db.close()
  
  return render_template('tags.html', tags=tags)
  
from flask import Blueprint, render_template

from app.db import DB

tag = Blueprint(
  'tag', __name__,
  template_folder='templates'
)

@tag.route('/tag/<tag_id>')
def tag_page(tag_id):
  db = DB("SELECT * FROM tags WHERE id = %s", [tag_id])
  tag = db.getOne()

  if tag == None:
    db.close()
    return ('Not found', 404)

  print('tag', tag)

  db.execute("SELECT url FROM links WHERE tag_id = %s ORDER BY random() LIMIT 1", [tag['id']])
  link = db.getOne()
  
  db.close()
  
  return render_template('tag.html', tag=tag, link=link)
  
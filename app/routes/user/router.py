from flask import Blueprint, render_template

from app.db import DB

user = Blueprint(
  'user', __name__,
  template_folder='templates'
)

@user.route('/user/<user_id>')
def user_page(user_id):
  db = DB("SELECT id, username FROM users WHERE id = %s", [user_id])
  user = db.getOne()

  if user == None:
    db.close()
    return ('Not found', 404)

  db.execute("""
    SELECT DISTINCT tags.title
      FROM tags
      JOIN links
        ON tags.id = links.tag_id
     WHERE links.user_id = %s
  """, [user_id])
  tags = db.getAll()

  db.execute("SELECT url FROM links WHERE user_id = %s ORDER BY random() LIMIT 1", [user_id])
  link = db.getOne()
  
  db.close()
  
  return render_template('user.html', user=user, tags=tags, link=link)
  
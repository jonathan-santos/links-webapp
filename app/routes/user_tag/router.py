from flask import Blueprint, render_template

from app.db import DB

user_tag = Blueprint(
  'user_tag', __name__,
  template_folder='templates'
)

@user_tag.route('/user/<user_id>/tag/<tag_id>')
def user_tag_page(user_id, tag_id):
  db = DB("SELECT username FROM users WHERE id = %s", [user_id])
  user = db.getOne()

  if user == None:
    db.close()
    return ('Not found', 404)

  db.execute("SELECT title FROM tags WHERE id = %s", [tag_id])
  tag = db.getOne()

  if tag == None:
    db.close()
    return ('Not found', 404)

  db.execute("""
    SELECT links.url
      FROM links
     WHERE links.user_id = %s AND links.tag_id = %s
  ORDER BY random()
     LIMIT 1
  """, [user_id, tag_id])
  link = db.getOne()

  db.close()

  title = f"{user['username']} - {tag['title']}"
  
  return render_template('user_tag.html', user=user, link=link, tag=tag, title=title)
  
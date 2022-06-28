from flask import Blueprint, render_template

from app.db import DB

users = Blueprint(
  'users', __name__,
  template_folder='templates'
)

@users.route('/users/<user_id>/')
def user_page(user_id):
  db = DB("SELECT id, username FROM users WHERE id = %s", [user_id])
  user = db.getOne()

  if user == None:
    db.close()
    return ('Not found', 404)

  db.execute("""
    SELECT DISTINCT tags.tagname
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
  
@users.route('/users/<user_id>/tag/<tag_id>')
def user_tag_page(user_id, tag_id):
  db = DB("SELECT username FROM users WHERE id = %s", [user_id])
  user = db.getOne()

  if user == None:
    db.close()
    return ('Not found', 404)

  db.execute("SELECT tagname FROM tags WHERE id = %s", [tag_id])
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

  title = f"{user['username']} - {tag['tagname']}"
  
  return render_template('user_tag.html', user=user, link=link, tag=tag, title=title)
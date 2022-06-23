from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from re import match

from app.db import DB
from app.utils import clean_string

links_new = Blueprint(
  'links_new', __name__,
  template_folder='templates'
)

@login_required
@links_new.route('/links/new', methods=['GET', 'POST'])
def links_new_page():
  if (request.method == 'GET'):
    return render_template('links_new.html')
  
  link = request.form.get('link', '')
  tag = request.form.get('tag', '')

  if not link:
      return ("link cannot be empty", 400)

  if not match("^(http(s)?:\/\/)+[\w\-\._~:\/?#[\]@!\$&'\(\)\*\+,;=.]+$", link):
    return ("links is invalid", 400)

  db = DB()

  tag_id = 1 # untagged

  if tag:
    if len(tag) < 2:
      db.close()
      return ("tag length cannot be lower than 2", 400)

    if len(tag) > 50:
      db.close()
      return ("tag length cannot be greater than 50", 400)

    db.execute("SELECT id FROM tags WHERE title = %s", [tag])

    tag_result = db.getOne()

    if tag_result == None:
      db.execute("""
        INSERT INTO tags (title, created_at)
        VALUES (%s, NOW())
        RETURNING id
      """, [clean_string(tag)])

      tag_result = db.getOne()

      db.save()

    tag_id = tag_result[0]

  db.execute("""
    INSERT INTO links (url, tag_id, user_id, created_at, updated_at)
    VALUES (%s, %s, %s, NOW(), NOW())
    RETURNING id
  """, [clean_string(link), tag_id, current_user.id])

  db.save()
  db.close()

  return ('OK', 200)

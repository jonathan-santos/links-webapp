from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from re import match

from ...db import DB

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

  if not link:
      return ("link cannot be empty", 400)

  if not match("^(http(s)?:\/\/)+[\w\-\._~:\/?#[\]@!\$&'\(\)\*\+,;=.]+$", link):
    return ("links is invalid", 400)

  db = DB("""
    INSERT INTO links (url, tag_id, user_id, created_at, updated_at)
    VALUES (%s, %s, %s, NOW(), NOW())
    RETURNING id
  """, [link, 1, current_user.id])

  db.save()
  db.close()

  return ('OK', 200)

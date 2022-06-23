from flask import Blueprint, render_template, request
from flask_login import login_required

from app.db import DB
from app.utils import clean_string

tags_new = Blueprint(
  'tags_new', __name__,
  template_folder='templates'
)

@login_required
@tags_new.route('/tags/new', methods=['GET', 'POST'])
def tags_new_page():
  if (request.method == 'GET'):
    return render_template('tags_new.html')
  
  tag = request.form.get('tag', '')

  if not tag:
      return ("tag cannot be empty", 400)

  if len(tag) < 2:
    return ("tag length cannot be lower than 2", 400)

  if len(tag) > 50:
    return ("tag length cannot be greater than 50", 400)

  db = DB("""
    INSERT INTO tags (title, created_at)
    VALUES (%s, NOW())
    RETURNING id
  """, [clean_string(tag)])

  db.save()
  db.close()

  return ('OK', 200)

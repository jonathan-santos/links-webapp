from flask import Blueprint, render_template, request
from flask_login import login_required

from app.db import DB
from app.utils import clean_string

tags = Blueprint(
  'tags', __name__,
  template_folder='templates'
)

@tags.route('/tags/')
def tags_page():
  db = DB("SELECT tagname from tags")
  tags = db.getAll()
  db.close()
  
  return render_template('tags.html', tags=tags)

@tags.route('/tags/<tag_id>')
def tag_page(tag_id):
  db = DB("SELECT * FROM tags WHERE id = %s", [tag_id])
  tag = db.getOne()

  if tag == None:
    db.close()
    return ('Not found', 404)

  db.execute("SELECT url FROM links WHERE tag_id = %s ORDER BY random() LIMIT 1", [tag['id']])
  link = db.getOne()
  
  db.close()
  
  return render_template('tag.html', tag=tag, link=link)
  
@login_required
@tags.route('/tags/new', methods=['GET', 'POST'])
def tags_new_page():
  if (request.method == 'GET'):
    return render_template('new_tag.html')
  
  tag = request.form.get('tag', '')

  if not tag:
      return ("tag cannot be empty", 400)

  if len(tag) < 2:
    return ("tag length cannot be lower than 2", 400)

  if len(tag) > 50:
    return ("tag length cannot be greater than 50", 400)

  db = DB("""
    INSERT INTO tags (tagname, created_at)
    VALUES (%s, NOW())
    RETURNING id
  """, [clean_string(tag)])

  db.save()
  db.close()

  return ('OK', 200)
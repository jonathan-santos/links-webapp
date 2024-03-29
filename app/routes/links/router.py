from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from re import match

from app.db import DB
from app.utils import clean_string

links = Blueprint(
  'links', __name__,
  template_folder='templates'
)

@links.route('/links/new', methods=['GET', 'POST'])
@login_required
def links_new_page():
  if (request.method == 'GET'):
    return render_template('links_new.html')
  
  link = request.form.get('link', '')
  tag = request.form.get('tag', '')

  if not link:
      return ("link cannot be empty", 400)

  if not match("(\b(https?|ftp|file)://)?[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]", link):
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

    db.execute("SELECT id FROM tags WHERE tagname = %s", [tag])

    tag_result = db.getOne()

    if tag_result == None:
      db.execute("""
        INSERT INTO tags (tagname, created_at)
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

  link_id = db.getOne()[0]

  db.save()
  db.close()

  return redirect(url_for("account.account_links_page"))

@links.route('/links/edit/<link_id>', methods=['GET', 'POST'])
@login_required
def links_edit_page(link_id):
  db = DB()

  if (request.method == 'GET'):
    db.execute("""
    SELECT links.id, links.url, tags.tagname
      FROM links
      JOIN tags
        ON links.tag_id = tags.id
     WHERE links.id = %s AND links.user_id = %s
    """, [link_id, current_user.id])

    link = db.getOne()

    db.close()

    if not link:
      return ('Not found', 404)

    return render_template('links_edit.html', link=link)

  link = request.form.get('link', '')
  tag = request.form.get('tag', '')

  if not link:
    db.close()
    return ("link cannot be empty", 400)

  if not match("^(http(s)?:\/\/)+[\w\-\._~:\/?#[\]@!\$&'\(\)\*\+,;=.]+$", link):
    db.close()
    return ("links is invalid", 400)

  tag_id = 1 # untagged

  if tag:
    if len(tag) < 2:
      db.close()
      return ("tag length cannot be lower than 2", 400)

    if len(tag) > 50:
      db.close()
      return ("tag length cannot be greater than 50", 400)

    db.execute("SELECT id FROM tags WHERE tagname = %s", [tag])

    tag_result = db.getOne()

    if tag_result == None:
      db.execute("""
        INSERT INTO tags (tagname, created_at)
        VALUES (%s, NOW())
        RETURNING id
      """, [clean_string(tag)])

      tag_result = db.getOne()

      db.save()

    tag_id = tag_result[0]

  db.execute("""
    UPDATE links
       SET url = %s, tag_id = %s, updated_at = NOW()
     WHERE id = %s
  """, [clean_string(link), tag_id, link_id])

  db.save()
  db.close()

  return redirect(url_for("account.account_links_page"))

@links.route('/links/delete/<link_id>', methods=['POST'])
@login_required
def links_delete(link_id):
  db = DB()

  db.execute("""
  SELECT links.id, links.url, tags.tagname
    FROM links
    JOIN tags
      ON links.tag_id = tags.id
    WHERE links.id = %s AND links.user_id = %s
  """, [link_id, current_user.id])

  link = db.getOne()

  if not link:
    return ('Not found', 404)

  db.execute("""
    DELETE FROM links
          WHERE id = %s
  """, [link_id])

  db.save()
  db.close()

  return redirect(url_for("account.account_links_page"))

from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.db import DB

user_links = Blueprint(
  'user_links', __name__,
  template_folder='templates'
)

@login_required
@user_links.route('/user/links')
def user_links_page():
  db = DB("""
    SELECT links.id, links.url, tags.title
      FROM links
      JOIN tags
        ON links.tag_id = tags.id
     WHERE user_id = %s
    """, [current_user.id])
  links = db.getAll()
  db.close()

  print("links",links)
  
  return render_template('user_links.html', links=links)
  
from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.db import DB

account = Blueprint(
  'account', __name__,
  template_folder='templates'
)

@login_required
@account.route('/account/links/')
def account_links_page():
  db = DB("""
    SELECT links.id, links.url, tags.title
      FROM links
      JOIN tags
        ON links.tag_id = tags.id
     WHERE user_id = %s
    """, [current_user.id])
  links = db.getAll()
  db.close()

  return render_template('account_links.html', links=links)
  
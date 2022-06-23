from flask import Blueprint, render_template
from flask_login import login_required

links_new = Blueprint(
  'links_new', __name__,
  template_folder='templates'
)

@login_required
@links_new.route('/links/new')
def links_new_page():
  return render_template('links_new.html')
  
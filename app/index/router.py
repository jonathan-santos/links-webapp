from flask import Blueprint, render_template
from flask_login import login_required

index = Blueprint(
  'index', __name__,
  template_folder='templates'
)

@login_required
@index.route('/')
def index_page():
  return render_template('index.html')
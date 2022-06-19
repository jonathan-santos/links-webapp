from flask import Blueprint, redirect
from flask_login import login_required, logout_user

logout = Blueprint(
  'logout', __name__,
  template_folder='templates'
)

@login_required
@logout.route('/logout')
def logout_page():
  logout_user()
  return redirect('/')

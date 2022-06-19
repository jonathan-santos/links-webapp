from flask import Blueprint, redirect
from flask_login import login_required, logout_user

logout = Blueprint('logout', __name__)

@logout.route('/logout')
@login_required
def logout_page():
  logout_user()
  return redirect('/')

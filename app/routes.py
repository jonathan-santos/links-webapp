from flask_login import login_required, logout_user
from flask import redirect

def create_routes(app):
  @app.route('/logout')
  @login_required
  def logout():
    logout_user()
    return redirect('/')

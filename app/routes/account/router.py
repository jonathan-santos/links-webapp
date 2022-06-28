from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from re import match

from app.db import DB

account = Blueprint(
  'account', __name__,
  template_folder='templates'
)

@login_required
@account.route('/account/', methods=['GET', 'POST'])
def account_page():
  if (request.method == 'GET'):
    return render_template('account.html', account=current_user)

  username = request.form.get("username", "")
  email = request.form.get("email", "")
  password = request.form.get("password", "")
  new_password = request.form.get("new-password", "")

  if not username:
      return ("username cannot be empty", 400)

  if len(username) < 2:
    return ("username length cannot be lower than 2", 400)

  if len(username) > 50:
    return ("username length cannot be greater than 50", 400)

  if not email:
      return ("email cannot be empty", 400)

  if not match('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email):
    return ("email is invalid", 400)

  if len(email) > 50:
    return ("email length cannot be greater than 255", 400)

  password_hash = current_user.password

  if new_password:
    if not password:
      return ("To change your password, you need to type your current password", 400)

    if len(new_password) < 2:
      return ("new password length cannot be lower than 2", 400)

    if len(new_password) > 50:
      return ("new password length cannot be greater than 50", 400)
    
    if not check_password_hash(current_user.password, password):
      return ("wrong password", 400)

    password_hash = generate_password_hash(new_password)

  # Update user account
  db = DB("""
    UPDATE users
       SET username = %s, email = %s, password = %s
     WHERE id = %s
    """, [username, email, password_hash, current_user.id])

  db.save()
  db.close()

  return ('OK', 200)

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
  
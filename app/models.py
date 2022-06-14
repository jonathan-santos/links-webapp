class User ():
  def __init__(self, id, username, email):
    self.id = id
    self.username = username
    self.email = email
    self.is_authenticated = True
    self.is_active = True
    self.is_anonymous = False

  def get_id(self):
    return str(self.id)
    
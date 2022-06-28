from .index.router import index
from .auth.router import auth
from .links.router import links
from .account.router import account
from .tags.router import tags
from .users.router import users

routes = [
  index,
  auth,
  links,
  account,
  tags,
  users,
]
from .index.router import index
from .auth.router import auth
from .links.router import links
from .user_links.router import user_links
from .tags.router import tags
from .users.router import users

routes = [
  index,
  auth,
  links,
  user_links,
  tags,
  users,
]
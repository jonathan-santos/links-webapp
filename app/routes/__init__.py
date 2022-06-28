from .index.router import index
from .register.router import register
from .login.router import login
from .logout.router import logout
from .links.router import links
from .user_links.router import user_links
from .tags.router import tags
from .users.router import users

routes = [
  index,
  register,
  login,
  logout,
  links,
  user_links,
  tags,
  users,
]
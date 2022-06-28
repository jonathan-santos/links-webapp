from .index.router import index
from .register.router import register
from .login.router import login
from .logout.router import logout
from .links_new.router import links_new
from .links_edit.router import links_edit
from .user_links.router import user_links
from .tags.router import tags
from .users.router import users

routes = [
  index,
  register,
  login,
  logout,
  links_new,
  links_edit,
  user_links,
  tags,
  users,
]
from .index.router import index
from .register.router import register
from .login.router import login
from .logout.router import logout
from .links_new.router import links_new
from .links_edit.router import links_edit
from .user_links.router import user_links
from .tag.router import tag
from .tags.router import tags
from .tags_new.router import tags_new
from .user.router import user
from .user_tag.router import user_tag

routes = [
  index,
  register,
  login,
  logout,
  links_new,
  links_edit,
  user_links,
  tag,
  tags,
  tags_new,
  user,
  user_tag
]
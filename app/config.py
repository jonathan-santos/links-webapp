from os import environ

def load_config(app):
  app.config['SECRET_KEY'] = environ['SECRET_KEY']

from os import path, environ
from sys import exit
from dotenv import load_dotenv

def load_config(app):
  if not path.isfile(".env"):
      print("\nNo '.env' file found.\n Exiting...\n")
      exit(4)

  load_dotenv()

  app.config['SECRET_KEY'] = environ['SECRET_KEY']

import os
import sys

from dotenv import load_dotenv

def load_config(app):
  if not os.path.isfile(".env"):
      print("\nNo '.env' file found.\n Exiting...\n")
      sys.exit(4)

  load_dotenv()

  app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

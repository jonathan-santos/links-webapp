import psycopg2
import os

def get_db_connection():
    con = psycopg2.connect(
      dbname=os.environ['DB_DATABASE'],
      user=os.environ['DB_USER'],
      password=os.environ['DB_PASSWORD'],
      host=os.environ['DB_HOST']
    )

    return con
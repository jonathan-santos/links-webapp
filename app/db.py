from psycopg2 import connect
from os import environ

class DB:
  def __init__(self, query = None, params = []):
    self.conn = self.connect()
    self.cur = self.conn.cursor() #cursor_factory=DictCursor

    if (query):
      self.execute(query, params)

  def connect(self):
    return connect(
      dbname=environ['DB_DATABASE'],
      user=environ['DB_USER'],
      password=environ['DB_PASSWORD'],
      host=environ['DB_HOST']
    )

  def execute(self, query, params = []):
    self.cur.execute(query, params)

  def getOne(self):
    return self.cur.fetchone()

  def getAll(self):
    return self.cur.fetchall()

  def save(self):
    self.conn.commit()

  def close(self):
    self.cur.close()
    self.conn.close()

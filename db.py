import psycopg2
from psycopg2.extras import RealDictCursor
import os

def getDb():
  db = psycopg2.connect(os.environ.get('DATABASE_URL'), cursor_factory=RealDictCursor)
  conn = db.cursor(cursor_factory=RealDictCursor)
  return conn ,db
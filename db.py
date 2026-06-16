import psycopg2
from psycopg2.extras import RealDictCursor
import os

def getDb():
  conn = psycopg2.connect(os.environ.get('DATABASE_URL'), cursor_factory=RealDictCursor)
  db = conn.cursor(cursor_factory=RealDictCursor)
  return conn, db
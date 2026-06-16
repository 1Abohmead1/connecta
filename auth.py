from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from db import getDb

def checkUser(username, email, password):
  conn, db = getDb()
  if not email: return "email is required!"
  if not username: return "username is required!"
  if not password: return "password is required!"

  db.execute('SELECT * FROM users WHERE username = %s AND email = %s', (username, email))
  user = db.fetchone()
  if not user: return "username or/and email not correct"

  if not check_password_hash(user[3], str(password)): return "password not correct"

  return user['user_id']

def availableEmail(email):
  conn, db = getDb()
  if not email: return "email is required"

  db.execute('SELECT * FROM users WHERE email = %s', (email,))
  if db.fetchone():
    return False
  
  return True

def availableUsername(username):
  conn, db = getDb()
  if not username: return "username is required"

  db.execute('SELECT * FROM users WHERE username = %s', (username,))
  if db.fetchone():
    return False
  
  return True

def registerUser(email, username, password, birth_day):
  if not availableEmail(email):
    return "email is already used"
  if not availableUsername(username):
    return "username is already used"
  if not birth_day:
    return "birth_day is required!" 

  if not password:
    return "password is required!"
  conn, db = getDb()

  try:
    db.execute(
      """INSERT INTO users (email, username, hash, birth, age) 
      VALUES(%s, %s, %s, %s, %s)""",
        (
          email,
          username, 
          generate_password_hash(password), 
          birth_day, 
          datetime.datetime.now().year - int(birth_day[0:4]),
        )
      )
    

    conn.commit()
  except:
    conn.rollback()
    return 'something went wrong please try again letter'
  
  db.execute('SELECT id FROM users WHERE email = %s', (email,))
  
  user_id = db.fetchone()['id']
  conn.close()

  try:
    return user_id
  except:
    return 'something went wrong please try again later!'

def loginUser(email, username, password):
  result = checkUser(username, email, password)

  try:
    return result
  except:
    return "something went wrong please try again later!"
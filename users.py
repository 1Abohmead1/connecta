from flask import session, current_app as app
from db import getDb
from upload import allowed_file, save_file
from auth import availableUsername
import cloudinary
import cloudinary.uploader

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def get_current_user():
  conn, db = getDb()

  try:
    db.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
    current_user = db.fetchone()
    return current_user
  except:
    return None
  finally:
    conn.close()
  
def get_user(username):
  if not username: return 'error'

  conn, db = getDb()

  try:
    db.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = db.fetchone()
    return user
  except ValueError:
    conn.rollback()
    return None
  finally:
    conn.close()
  
def update_user(username, user_image, profile_image, bio):
  current_user = get_current_user()
  if username != current_user['username']:
    if not availableUsername(username):
      return 'username is already used'
    
  did_no_changes = username == current_user['username'] and not user_image and not profile_image and not bio
  
  if did_no_changes:
    return "you haven't change any thing"

  conn, db = getDb()

  try:
    if username:
      db.execute('UPDATE users SET username = %s WHERE id = %s', (username, session['user_id'],))
    if user_image and allowed_file(user_image.filename, ALLOWED_EXTENSIONS):
      old_image = current_user['user_image_path']
      if old_image and 'cloudinary' in old_image:
        public_id = old_image.split('/')[-1].split('.')[0]
        cloudinary.uploader.destroy(public_id)
      user_image_path = save_file(user_image)
      db.execute('UPDATE users SET user_image_path = %s WHERE id = %s', (user_image_path, session['user_id'],))
    if profile_image and allowed_file(profile_image.filename, ALLOWED_EXTENSIONS):
      profile_image_path = save_file(profile_image)
      db.execute('UPDATE users SET profile_image_path = %s WHERE id = %s', (profile_image_path, session['user_id'],))
    if bio:
      db.execute('UPDATE users SET bio = %s WHERE id = %s', (bio, session['user_id'],))

    conn.commit()
    return 'success'
  except Exception as e:
    print(f'[ERROR] {e}')
    conn.rollback()
    return 'some thing went wrong please try again later!'
  finally:
    conn.close()

def get_user_posts(username):
  if not username: 
    return None

  conn, db = getDb()

  try:
    user = get_user(username)
    if not user: 
      return None
    
    db.execute(
      '''
      SELECT posts.id,
      posts.user_id,
      users.username,
      users.email,
      users.user_image_path,
      posts.post_content,
      posts.post_likes,
      posts.post_dislikes,
      posts.post_laughs,
      posts.post_date,
      posts.post_image_path FROM posts
      JOIN users ON users.id = posts.user_id
      WHERE users.username = %s
      ORDER BY post_date DESC
      ''', (username,)
    )
    posts = db.fetchall()
    return posts
  except ValueError:
    conn.rollback()
    return None
  finally:
    conn.close()

def new_friend_request(user_id):
  if not user_id: return

  conn, db = getDb()

  try:
    already_request = friend_request(user_id) == 'receiver'
    if already_request: return

    db.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = db.fetchone()
    if not user: return

    db.execute(
      '''
      INSERT INTO friends 
      (
      sender_id, 
      receiver_id
      ) VALUES (%s, %s)
      ''', (session['user_id'], user_id,)
    )

    conn.commit()
  except:
    conn.rollback()
    return
  finally:
    conn.close()

  return 'success'

def friend_request(user_id):
  if not user_id: 
    return False

  conn, db = getDb()
  try:
    db.execute(
      '''SELECT sender_id FROM friends 
      WHERE (
      receiver_id = %s AND sender_id = %s
      OR sender_id = %s AND receiver_id = %s
      )
      AND status = 'request'
      ''', (session['user_id'], user_id, session['user_id'], user_id,)
    )
    row = db.fetchone()
    if not row:
      return False
    sender_id = row['sender_id']
    if sender_id == session['user_id']:
      return 'sender'
    elif sender_id == user_id:
      return 'reciever'
    return False
  except:
    return False
  finally:
    conn.close()

def get_friends(user_id):
  conn, db = getDb()

  try:
    db.execute(
      '''
      SELECT * 
      FROM users JOIN friends ON (
      users.id = friends.sender_id OR
      users.id = friends.receiver_id
      )
      WHERE (
        friends.sender_id = %s
        OR friends.receiver_id = %s
      )
      AND friends.status = 'friends'
      AND users.id != %s
      ''', (user_id, user_id, user_id,)
    )
    friends = db.fetchall()
    return friends
  except:
    return None
  finally:
    conn.close()

def get_friend_requests():
  conn, db = getDb()

  try:
    db.execute(
      '''
      SELECT * 
      FROM users JOIN friends ON users.id = friends.sender_id 
      WHERE friends.status = 'request'
      AND friends.receiver_id = %s
      ''', (session['user_id'],)
    )
    requests = db.fetchall()
    return requests
  except:
    return None
  finally:
    conn.close()

def new_friend(user_id):
  if not user_id: 
    return

  conn, db = getDb()
  try:
    db.execute("UPDATE friends SET status = 'friends' WHERE sender_id = %s AND receiver_id = %s", (user_id, session['user_id'],))
    conn.commit()
  except:
    conn.rollback()
    return
  finally:
    conn.close()

def delete_friend(friend_id):
  if not friend_id: return

  conn, db = getDb()
  try:
    db.execute('SELECT * FROM users WHERE id = %s', (friend_id,))
    current_friend = db.fetchone()
    if not current_friend: return

    db.execute(
      '''
      DELETE FROM friends 
      WHERE (
      receiver_id = %s AND sender_id = %s 
      OR sender_id = %s AND receiver_id = %s
      )
      ''', (friend_id, session['user_id'], friend_id, session['user_id'],)
    )

    conn.commit()
  except Exception as e:
    conn.rollback()
    return
  finally:
    conn.close()

def is_friends(user_id):
  if not user_id: 
    return False
  
  conn, db = getDb()

  try:
    db.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = db.fetchone()
    if not user:
      return False

    db.execute(
      '''
      SELECT status FROM friends 
      WHERE (
        sender_id = %s AND receiver_id = %s
        OR receiver_id = %s AND sender_id = %s
      )
      ''', (session['user_id'], user_id, session['user_id'], user_id,)
    )
    row = db.fetchone()
    if not row:
      return False

    if row['status'] == 'friends':
      return True
    
    return False
  except Exception:
    return False
  finally:
    conn.close()
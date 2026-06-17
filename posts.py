from db import getDb
from flask import session, current_app as app, jsonify
from upload import save_file, allowed_file

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def newPost(post_content, post_image):
  if not post_content: return "post content is required"

  try:
    conn, db = getDb()

    if post_image and post_image.filename != '':

      if allowed_file(post_image.filename, ALLOWED_EXTENSIONS):
        post_image_path = save_file(post_image)
      else:
        return "Invalid file type. Allowed types are: {}".format(', '.join(ALLOWED_EXTENSIONS))

      db.execute(
        """
        INSERT INTO posts 
        (
          user_id, 
          post_content, 
          post_image_path
        )
        VALUES (%s, %s, %s)
        """,
        (session['user_id'], post_content, post_image_path,)
      )
    else:
      db.execute(
        """
        INSERT INTO posts 
        (
          user_id, 
          post_content
        )
        VALUES (%s, %s)
        """,
        (session['user_id'], post_content,)
      )

    conn.commit()
    return 'success'
  except:
    conn.rollback()
    return 'something went wrong please try again later'
  finally:
    conn.close()

def getPosts():
  conn, db = getDb()

  try:
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
      post_image_path FROM posts
      JOIN users ON users.id = posts.user_id
      ORDER BY post_date DESC
      '''
    )
    posts = db.fetchall()
    return posts
  except:
    return None
  finally:
    conn.close()

def getReacts():
  conn, db = getDb()

  try:
    db.execute('SELECT * FROM reacts')
    reacts = db.fetchall()
    return reacts
  except:
    conn.rollback()
    return 'error'
  finally:
    conn.close()

def isReacted(post_id, react):
  if not post_id or not react: return False

  conn, db = getDb()
  db.execute(
    '''
     SELECT * FROM reacts 
     WHERE user_id = %s 
     AND post_id = %s 
     AND react = %s
     ''', (session['user_id'], post_id, react,)
  )
  reacted = db.fetchone()
  
  conn.close()

  if not reacted:
    return False
  
  return True

def reactPost(react, csrf, post_id):
  valid_reacts = ['like', 'dislike', 'laugh', 'reset']
  conn, db = getDb()

  print(f'[DEBUG] react: {react}')
  print(f'[DEBUG] csrf received: {csrf}')
  print(f'[DEBUG] csrf in session: {session.get("csrf_token")}')
  print(f'[DEBUG] post_id: {post_id}')

  if not react or react not in valid_reacts:
    print('[DEBUG] failed: invalid react')
    return 'error'
  
  if not csrf or csrf != session['csrf_token']:
    print('[DEBUG] failed: csrf mismatch')
    return 'error'
  
  db.execute('SELECT * FROM posts WHERE id = %s', (post_id,))
  current_post = db.fetchone()
  if not post_id or not current_post:
    print('[DEBUG] failed: post not found')
    return jsonify({'error': 'some thing went wrong'})
  
  try:
    db.execute('DELETE FROM reacts WHERE user_id = %s AND post_id = %s', (session['user_id'], post_id,))
    
    if react != 'reset':
      db.execute(
        '''INSERT INTO reacts 
        (
          user_id,
          post_id, 
          react
        )
        VALUES (%s, %s, %s)
        ''', (session['user_id'], post_id, react)
      )
    
    db.execute('SELECT COUNT(*) as count FROM reacts WHERE react = %s AND post_id = %s', ('like', post_id,))
    post_likes = int(db.fetchone()['count'])
    print(f'[DEBUG] new post_like {post_likes}')

    db.execute('SELECT COUNT(*) as count FROM reacts WHERE react = %s AND post_id = %s', ('dislike', post_id,))
    post_dislikes = int(db.fetchone()['count'])
    print(f'[DEBUG] new post_like {post_dislikes}')

    db.execute('SELECT COUNT(*) as count FROM reacts WHERE react = %s AND post_id = %s', ('laugh', post_id,))
    post_laughs = int(db.fetchone()['count'])
    print(f'[DEBUG] new post_laughs {post_laughs}')

    db.execute(
      '''
       UPDATE posts
       SET post_likes = %s,
       post_dislikes = %s,
       post_laughs = %s
       WHERE id = %s
       ''', (post_likes, post_dislikes, post_laughs, post_id,)
    )
    
    conn.commit()
  except Exception as e:
    conn.rollback()
    print(f'[ERROR] {e}')
    return jsonify({'error': 'some thing went wrong'})
  finally:
    conn.close()

  return jsonify([post_likes, post_dislikes, post_laughs])

def newPostComment(post_id, content):
  if not post_id or not content: return 

  conn, db = getDb()

  db.execute('SELECT * FROM posts WHERE id = %s', (post_id,))
  post = db.fetchone()
  if not post:
    return 'error'
  
  try:
    db.execute(
      'INSERT INTO comments (user_id, post_id, content) VALUES (%s, %s, %s) RETURNING id',
      (session['user_id'], post_id, content,)
    )
    new_comment_id = db.fetchone()['id']
    conn.commit()
  except:
    conn.rollback()
    return 'error'

  db.execute(
    '''
    SELECT username, content, date, user_image_path
    FROM users JOIN comments ON users.id = comments.user_id
    WHERE comments.id = %s
    ''', (new_comment_id,)
  )
  new_comment = db.fetchone()
  
  conn.close()

  return jsonify({
    'id': new_comment_id,
    'username': new_comment['username'],
    'content': new_comment['content'],
    'date': new_comment['date'],
    'user_image': new_comment['user_image_path']
  })

def getComments(post_id):
  if not post_id: 
    return None

  conn, db = getDb()

  try:
    db.execute(
      '''
      SELECT comments.id,
      comments.content,
      comments.user_id,
      users.username,
      users.user_image_path,
      comments.date FROM users JOIN comments ON users.id = comments.user_id
      WHERE post_id = %s
      ORDER BY date DESC
      ''', (post_id,)
    )
    comments = db.fetchall()
    return comments, len(comments)
  except:
    return None, 0
  finally:
    conn.close()

def removePostComment(comment_id):
  if not comment_id: return 'error'
  print(f'[DEBUG] comment_id = {comment_id}')

  conn, db = getDb()

  try:
    db.execute('DELETE FROM comments WHERE id = %s', (comment_id,))
    conn.commit()
    print('[DEBUG] database commited')
    return 'success'
  except Exception as e:
    conn.rollback()
    print(f'[DEBUG] error: {e}')
    return 'error'
  finally:
    conn.close()
    print('[DEBUG] database closed')

def remove_post(post_id):
  print(f'[DEBUG] post_id: {post_id}')
  if not post_id: return 'error'

  conn, db = getDb()

  try:
    db.execute('DELETE FROM reacts WHERE post_id = %s', (post_id,))
    db.execute('DELETE FROM posts WHERE id = %s', (post_id,))
    db.execute('DELETE FROM comments WHERE post_id = %s', (post_id,))
    conn.commit()
    return 'success'
  except Exception as e:
    print(f'[ERROR] {e}')
    conn.rollback()
    return 'some thing went wrong'
  finally:
    conn.close()
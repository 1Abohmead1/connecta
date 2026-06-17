from db import getDb
from flask import session, jsonify
from upload import save_file, allowed_file

ALLOWED_EXTENSIONS = {'mp4', 'mkv'}

def new_status(video):
  if not video: 
    return 'no status video provided !'

  conn, db = getDb()

  try:
    if not allowed_file(video.filename, ALLOWED_EXTENSIONS) or video.filename == '':
      return 'Invalid file type. Allowed types are: {}'.format(', '.join(ALLOWED_EXTENSIONS))

    print(f'[DEBUG] uploading video: {video.filename}')
    video_path = save_file(video)
    print(f'[DEBUG] upload success: {video_path}')

    db.execute('UPDATE users SET status_video_path = %s WHERE id = %s', (video_path, session['user_id'],))
    conn.commit()

    return 'success'
  except Exception as e:
    print(f'[ERROR] {e}')
    conn.rollback()
    return 'something went wrong please try again later!'
  finally:
    conn.close()

def removeStatus():
  conn, db = getDb()

  try:
    db.execute('UPDATE users SET status_video_path = NULL WHERE id = %s', (session['user_id'],))
    conn.commit()
  except:
    conn.rollback()
    return 'some thing went wrong please try again later !'
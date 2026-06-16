import secrets
import os
from flask import current_app as app

def allowed_file(filename, ALLOWED_EXTENSIONS):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file):
  random_hex = secrets.token_hex(8)
  _, f_ext = os.path.splitext(file.filename)
  file_name = random_hex + f_ext
  file_path = os.path.join(app.root_path, 'uploads/', file_name)
  file.save(file_path)
  return file_name

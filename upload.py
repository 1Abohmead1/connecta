import cloudinary
import cloudinary.uploader
import os

cloudinary.config(
  cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
  api_key=os.environ.get('CLOUDINARY_API_KEY'),
  api_secret=os.environ.get('CLOUDINARY_API_SECRET')
)

def allowed_file(filename, ALLOWED_EXTENSIONS):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file):
  result = cloudinary.uploader.upload(file)
  return result['secure_url']

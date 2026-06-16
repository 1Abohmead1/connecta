'''
══════ CONNECTA ══════════════════════════════════════════════
  professional social media platform, created with love,
  built with python with flask in backend, and html, css, javascript
  in frontend
══════════════════════════════════════════════════════════════
'''

from flask import Flask, render_template, request, session, flash, redirect, url_for, send_from_directory
from flask_session import Session
from flask_login import LoginManager, login_required, login_user, UserMixin, logout_user
from auth import registerUser, loginUser
from posts import newPost, getPosts, reactPost, isReacted, newPostComment, getComments, removePostComment, remove_post
import users
from status import new_status, removeStatus
import os
import secrets

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'C[*yttLv07qAK!ndIGBtsnvBS1F;bZJRmR,rK!bhc;#'
Session(app)

if __name__ == 'main':
  app.run()

@app.after_request
def no_cache(response):
  response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
  response.headers['Pragma'] = 'no-cache'
  response.headers['Expires'] = '0'
  return response

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
  def __init__(self, id):
    self.id = id

@login_manager.user_loader
def load_user(user_id):
  return User(user_id)

@app.route('/')
@app.route('/home')
@login_required
def home():
  posts = getPosts()
  current_user = users.get_current_user()
  friends = users.get_friends(session['user_id'])
  
  return render_template(
    'index.html', 
    posts=posts, 
    isReacted=isReacted, 
    getComments=getComments, 
    current_user=current_user,
    friends=friends
  )

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    return render_template('login.html')
  
  email = request.form.get('email')
  username = request.form.get('username')
  password = request.form.get('password')

  result = loginUser(email, username, password)
  
  try:
    user_id = int(result)
    login_user(User(user_id))
    session['user_id'] = user_id
    session['csrf_token'] = secrets.token_hex(16)
    return 'success'
  except:
    return str(result)

@app.route('/logout', methods=['POST'])
@login_required
def logout():
  logout_user()
  return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'GET':
    return render_template('register.html')
  
  email = request.form.get('email')
  username = request.form.get('username')
  password = request.form.get('password')
  birth_day = request.form.get('birth_day')
 
  result = registerUser(email, username, password, birth_day)
  try:
    user_id = int(result)
    login_user(User(user_id))
    session['user_id'] = user_id
    session['csrf_token'] = secrets.token_hex(16)
    return 'success'
  except:
    return str(result)

@app.route('/publish', methods=['POST'])
@login_required
def post():
  post_content = request.form.get('content')
  post_image = request.files['image']

  return newPost(post_content, post_image)

@app.route('/status/new', methods=['POST'])
@login_required
def upload_status():
  video = request.files['video']

  return new_status(video)

@app.route('/status/remove', methods=['POST'])
@login_required
def remove_status():
  removeStatus()

  flash('your status deleted !', 'success')
  return redirect('/')

@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
  upload_folder = os.path.join(app.root_path, 'uploads')
  return send_from_directory(upload_folder, filename)

@app.route('/posts/react', methods=['POST'])
@login_required
def react():
  react = request.form.get('react')
  csrf = request.form.get('csrf_token')
  post_id = request.form.get('post_id')

  return reactPost(react, csrf, post_id)

@app.route('/posts/comment/new', methods=['POST'])
@login_required
def new_comment():
  post_id = request.form.get('post_id')
  content = request.form.get('content')

  return newPostComment(post_id, content)

@app.route('/posts/comment/delete', methods=['POST'])
@login_required
def delete_comment():
  comment_id = request.form.get('comment_id')

  return removePostComment(comment_id)

@app.route('/posts/delete', methods=['POST'])
@login_required
def delete_post():
  post_id = request.form.get('post_id')

  return remove_post(post_id)

@app.route('/profile/<username>')
@login_required
def profile(username):
  current_user = users.get_current_user()
  
  user = users.get_user(username)
  posts = users.get_user_posts(username)
  friends = users.get_friends(user['id'])
  return render_template(
    'profile.html', 
    current_user=current_user, 
    user=user, 
    posts=posts, 
    isReacted=isReacted,
    getComments=getComments,
    friends=friends,
    friend_request=users.friend_request,
    is_friends=users.is_friends
  )

@app.route('/profile/')
def redirect_profile():
  user = users.get_current_user()
  return redirect(f'/profile/{user['username']}')

@app.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
  user_image = request.files['user-image']
  profile_image = request.files['profile-image']
  username = request.form.get('username')
  bio = request.form.get('bio')

  return users.update_user(username, user_image, profile_image, bio)

@app.route('/friends')
@login_required
def friends():
  friends = users.get_friends(session['user_id'])
  requests = users.get_friend_requests()

  return render_template('friends.html', friends=friends, requests=requests)

@app.route('/friends/request', methods=['POST'])
@login_required
def friend_request():
  user_id = request.form.get('user_id')

  return users.new_friend_request(user_id)

@app.route('/friends/new', methods=['POST'])
@login_required
def add_friend():
  user_id = request.form.get('user_id')

  users.new_friend(user_id)
  flash('new friend !', 'success')
  return redirect('/friends')

@app.route('/friends/remove', methods=['POST'])
@login_required
def remove_friend():
  user_id = request.form.get('user_id')

  users.delete_friend(user_id)
  flash('friend deleted !', 'success')
  return redirect('/friends')


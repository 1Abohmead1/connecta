# ═══ CONNECTA ══════════════════════════════════════════════
#### Video Demo: coming soon
#### Description:
Connecta is a social media platform where you can upload your status, publish posts, react on posts, and send comments.

Every user has an individual account with a unique email and username and a profile page that contains their personal information like their email, username, bio, friends, profile image, and user image. Only the user has the ability to edit their own profile and information.

Every post has four stats: likes, dislikes, laughs, and comments, and has its own comments section. You can create a category by typing '#category' in the post content. In the post header there is the information of the user who published the post, like their username, email, and the post publish time. The same applies to comments — they display the same information and are ordered by date DESC to show the newest comments first. You can include an image in your post and this image is scalable by clicking on it.

---

#### Technologies:
1. **HTML**: the web structure

in `/templates/` there are the HTML files:
  1. `index.html`: the home page that contains the sidebar, the header, and the page content like: friends' statuses, the add status form, and the add post form that contains the user image, the post content textarea, the publish button, and the error preview paragraph. And the page posts.
  2. `layout.html`: the global HTML layout file that all pages extend.
  3. `login.html`: the login page that contains the login form and authentication.
  4. `register.html`: the register page that contains the create new account form.
  5. `profile.html`: the user profile page — shows an update form if the user is viewing their own profile, and a profile preview for everyone else.
  6. `friends.html`: the friend requests and current friends page. In this page you can accept friend requests and remove current friends.

---

2. **CSS** (includes Bootstrap): the web styles

in `/static/css/` there are the CSS files:
  1. `components.css`: the main CSS file and the web components styles.
  2. `global.css`: the global CSS file that contains the main variables and user agent style overwrites.

---

3. **JavaScript**: the web frontend logic and backend fetching

in `/static/js/` there are the JS files:

  1. `auth.js`: the file which contains the login and register pages' dynamic design and backend register and login fetches.

      functions:
      1. `passwordShowButton()`: a simple function that displays the user's password after they enter it, by converting the password input type into a text input.
      2. `fieldsActivation()`: a simple function that activates the fields by adding 'active' to the input's classList by listening to user input and checking if there is a value to add or remove the active class. The active field styles are handled in the CSS components file.
      3. `fieldsValidation()`: the more complex function that makes validation checks on the inputs before sending the request to the backend. After checking every input it sends the form data to the backend and fetches the response. If the response is 'success' the function redirects the user to the home page. Otherwise it takes the response and checks if there is an input name in the response, then makes that field invalid with CSS. Every input has an error preview element under it — after receiving the error response it displays it in the field error preview and disables the submit button while listening for new user input.
      4. `newError()`: a helper function that creates and appends an error element to the error preview container and marks the input as invalid.
      5. `resetInput()`: a helper function that removes the invalid state from an input and clears its error preview.

  2. `components.js`: the file which contains the page element components like the custom HTML elements.

      functions:
      1. `logo()`: the function which creates the logo element. It is called in HTML by writing:
```html
      <logoContainer></logoContainer>
```
      2. `uploadBtn()`: the function which is responsible for the media upload button, like status videos and post images:
```html
      <button class="upload-btn">
        <input hidden type="file" name="image" accept=".jpg, .jpeg, .png">
        <i data-lucide="upload"></i>
      </button>
```
      3. `toggleBtnActivation()`: a simple function that toggles the 'active' class on toggle buttons when clicked.

  3. `home.js`: the file which contains the home page functions.

      functions:
      1. `postMediaSelection()`: the function which takes the post's selected image after the user chooses it via the upload button and displays it in the preview element before publishing.
      2. `postCategories()`: the function which makes post categories by searching for '#category' and converting it into a custom HTML element:
```html
      <category>#category</category>
```
      3. `postPublish()`: the function which handles post publishing by listening to the publish form submit event and validating that the textarea is not empty before submitting.
      4. `postReactions()`: the function which handles post reactions (like, dislike, laugh). It listens for reaction button clicks, sends a fetch request to `/posts/react` with the CSRF token, and updates the reaction counts on the page dynamically without a page reload.
      5. `postComments()`: the function which handles adding and removing comments. It listens for the comment form submit event, sends a fetch request to `/posts/comment/new`, and dynamically prepends the new comment to the comments list. It also handles comment deletion by sending a fetch request to `/posts/comment/delete` and removing the comment element from the DOM.
      6. `deletePost()`: the function which handles post deletion. It listens for the delete post form submit event, sends a fetch request to `/posts/delete`, and removes the post element from the DOM if the response is 'success'.
      7. `Status()`: the function which handles status video uploading. It listens for the status form submit event, triggers the file input click, and after the user selects a video it sends a fetch request to `/status/new` and reloads the page on success.
      8. `mediaScaling()`: the function which makes media elements (images, videos) scalable by clicking on them. It creates a scaled clone of the media element and appends it to the body with an overlay, and removes it when the user clicks the close button or the overlay.

  4. `profile.js`: the file which contains the profile page functions.

      functions:
      1. `friendRequest()`: the function which handles sending a friend request. It listens for the friend request form submit event, sends a fetch request to `/friends/request`, and updates the button state to 'friend request sent' after sending.
      2. `updateProfile()`: the function which handles profile updates. It listens for the update form submit event, sends a fetch request to `/profile/update` with the new profile data, and redirects to the profile page on success or displays the error message.

---

4. **Python with Flask**: backend logic and database control

in `/` there are the Python files:
4. **Python with Flask**: backend logic and database control

in `/` there are the Python files:
  1. `app.py`: the main Flask application file that contains all the routes and connects all the modules together.

      routes:
      1. `GET/POST /` and `/home`: the home page route that fetches all posts, the current user, and friends and passes them to the home template.
      2. `GET/POST /login`: the login page route that renders the login form on GET and handles login logic on POST by calling `loginUser()` and creating the user session.
      3. `POST /logout`: the logout route that logs out the current user and redirects to the login page.
      4. `GET/POST /register`: the register page route that renders the register form on GET and handles registration logic on POST by calling `registerUser()` and creating the user session.
      5. `POST /publish`: the post publishing route that gets the post content and image from the form and calls `newPost()`.
      6. `POST /status/new`: the status upload route that gets the video from the form and calls `new_status()`.
      7. `POST /status/remove`: the status remove route that calls `removeStatus()` and redirects to the home page.
      8. `GET /uploads/<filename>`: the file serving route that serves uploaded files from the uploads folder.
      9. `POST /posts/react`: the post reaction route that gets the react, CSRF token, and post id from the form and calls `reactPost()`.
      10. `POST /posts/comment/new`: the new comment route that gets the post id and content from the form and calls `newPostComment()`.
      11. `POST /posts/comment/delete`: the delete comment route that gets the comment id from the form and calls `removePostComment()`.
      12. `POST /posts/delete`: the delete post route that gets the post id from the form and calls `remove_post()`.
      13. `GET /profile/<username>`: the profile page route that fetches the user, their posts, and friends and passes them to the profile template.
      14. `GET /profile/`: the profile redirect route that redirects to the current user's profile page.
      15. `POST /profile/update`: the profile update route that gets the new profile data from the form and calls `update_user()`.
      16. `GET /friends`: the friends page route that fetches the current user's friends and friend requests and passes them to the friends template.
      17. `POST /friends/request`: the friend request route that gets the user id from the form and calls `new_friend_request()`.
      18. `POST /friends/new`: the add friend route that gets the user id from the form and calls `new_friend()` and redirects to the friends page.
      19. `POST /friends/remove`: the remove friend route that gets the user id from the form and calls `delete_friend()` and redirects to the friends page.

---

  2. `auth.py`: handles user authentication.

      functions:
      1. `checkUser(username, email, password)`: validates the user's credentials by checking if the username and email exist in the database and if the password matches the stored hash. Returns the user id on success or an error message on failure.
      2. `availableEmail(email)`: checks if the email is already used by another user in the database. Returns `True` if available or `False` if not.
      3. `availableUsername(username)`: checks if the username is already used by another user in the database. Returns `True` if available or `False` if not.
      4. `registerUser(email, username, password, birth_day)`: registers a new user by validating the email, username, password, and birth date, hashing the password with Werkzeug, and inserting the new user into the database. Returns the new user id on success or an error message on failure.
      5. `loginUser(email, username, password)`: logs in the user by calling `checkUser()` and returning the user id on success or an error message on failure.

---

  3. `users.py`: handles all user-related logic.

      functions:
      1. `get_current_user()`: fetches the current logged-in user from the database using the session user id. Returns the user row or `None` if not found.
      2. `get_user(username)`: fetches a user from the database by their username. Returns the user row or `None` if not found.
      3. `update_user(username, user_image, profile_image, bio)`: updates the current user's profile information. Checks if the new username is available, validates and saves any uploaded images, and updates the database. Returns 'success' or an error message.
      4. `get_user_posts(username)`: fetches all posts by a user ordered by date descending. Returns a list of post rows or `None` if not found.
      5. `new_friend_request(user_id)`: sends a friend request to another user by inserting a new row into the friends table with status 'request'. Returns 'success' or `None` on failure.
      6. `friend_request(user_id)`: checks the friend request status between the current user and another user. Returns 'sender' if the current user sent the request, 'receiver' if they received it, or `False` if there is no request.
      7. `get_freinds(user_id)`: fetches all friends of a user where the friendship status is 'friends'. Returns a list of user rows or `None` on failure.
      8. `get_friend_requests()`: fetches all pending friend requests received by the current user. Returns a list of user rows or `None` on failure.
      9. `new_friend(user_id)`: accepts a friend request by updating the friends table row status from 'request' to 'friends'.
      10. `delete_friend(friend_id)`: removes a friendship by deleting the friends table row between the current user and the given friend id.

---

  4. `posts.py`: handles all post-related logic.

      functions:
      1. `newPost(post_content, post_image)`: creates a new post by validating the content, optionally saving an uploaded image, and inserting the post into the database. Returns 'success' or an error message.
      2. `getPosts()`: fetches all posts joined with their authors ordered by date descending. Returns a list of post rows or `None` on failure.
      3. `getReacts()`: fetches all reactions from the database. Returns a list of react rows or an error message.
      4. `isReacted(post_id, react)`: checks if the current user has reacted to a post with a specific reaction type. Returns `True` or `False`.
      5. `reactPost(react, csrf, post_id)`: handles post reactions by validating the CSRF token and reaction type, deleting the previous reaction, inserting the new one, recalculating the reaction counts, and updating the post. Returns a list of `[likes, dislikes, laughs]` or an error message.
      6. `newPostComment(post_id, content)`: adds a new comment to a post by inserting it into the database and returning the new comment data as a JSON response.
      7. `getComments(post_id)`: fetches all comments for a post joined with their authors ordered by date descending. Returns a tuple of `(comments, count)`.
      8. `removePostComment(comment_id)`: deletes a comment from the database by its id. Returns 'success' or an error message.
      9. `remove_post(post_id)`: deletes a post and all its comments from the database. Returns 'success' or an error message.

---

  5. `status.py`: handles user status videos.

      functions:
      1. `new_status(video)`: uploads a new status video by validating the file extension, saving the file, and updating the user's status video path in the database. Returns 'error' on failure.
      2. `removeStatus()`: removes the current user's status video by setting the status video path to NULL in the database. Returns 'error' on failure.

---

  6. `upload.py`: handles file uploads.

      functions:
      1. `allowed_file(filename, ALLOWED_EXTENSIONS)`: checks if a file's extension is in the allowed extensions set. Returns `True` or `False`.
      2. `save_file(file)`: saves an uploaded file to the uploads folder with a random hex filename to avoid conflicts and returns the generated filename.

---

  7. `db.py`: database connection module.

      functions:
      1. `getDb()`: creates and returns a new SQLite database connection to `connecta.db` with the row factory set to `sqlite3.Row` so rows can be accessed like dictionaries.
---

5. **SQLite**: database

The database `connecta.db` contains the following tables:
  1. `users`: stores user information — id, email, username, password hash, bio, birth date, age, user image, profile image, status video, and creation date.
  2. `posts`: stores posts — id, user id, post content, post image, likes, dislikes, laughs, and post date.
  3. `comments`: stores comments — id, user id, post id, content, and date.
  4. `reacts`: stores reactions — id, user id, post id, and react type.
  5. `friends`: stores friend relationships — id, sender id, receiver id, and status ('request' or 'friends').

#### Design Touches:
1. i used custom html elements to write it once then javascript write it's content
2. i used `<pre>` html element to make the post content as entered by the user

# C O N N E C T A
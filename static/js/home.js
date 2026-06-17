function postMediaSelection() {
  const section = document.querySelector('.post-creation')
  if (!section) return
  const previewEl = section.querySelector('.post-image-preview')
  const imageInput = section.querySelector('input[name="image"]')

  imageInput.addEventListener('change', (event) => {
    imageInput.accept = 'image/*'
    const image = event.target.files[0]

    processImage(image)
  })

  function processImage(image) {
    const reader = new FileReader();
    reader.onloadend = (e) => {
      if (!reader.result) return;

      const imgEl = document.createElement('img');
      imgEl.src = e.target.result;
      previewEl.appendChild(imgEl);
    };

    reader.readAsDataURL(image);
  }
}

function postCategories() {
  const posts = document.querySelectorAll('.post .post-content')

  posts.forEach(post => {
    post.innerHTML = post.innerText.replaceAll(`#`, `<category>#`)
  })
}

function postPublish() {
  const form = document.querySelector('.new-post-form')
  if (!form) return
  const textarea = form.querySelector('textarea')
  const errorPreview = document.querySelector('.post-error-preview')

  form.addEventListener('submit', async (event) => {
    event.preventDefault()
    if (!textarea.value) {
      textarea.classList.add('invalid')
      return
    }

    const response = await fetch('/publish', {
      method: 'POST',
      body: new FormData(form)
    })

    const result = await response.text()

    if (result != 'success') {
      errorPreview.textContent = result
    } else {
      window.location.href = '/'
    }
  })
}

function postReactions() {
  const forms = document.querySelectorAll('.post-stats')
  if (!forms) return

  forms.forEach(form => {
    const btns = form.querySelectorAll('.post .post-btn')
    const reactInput = form.querySelector('input[name="react"]')

    btns.forEach(btn => {
      btn.addEventListener('click', () => {
        if (btn.classList.contains('active')) {
          btn.classList.remove('active')
          reactInput.value = 'reset'
          return
        }
        btns.forEach(btn => btn.classList.remove('active'))
        btn.classList.add('active')
      })
    })

    form.addEventListener('submit', async (event) => {
      event.preventDefault()
      btns.forEach(btn => {
      if (btn.classList.contains('active')) {
        reactInput.value = btn.dataset.reaction
      }
      })

      const response = await fetch(`/posts/react`, {
      method: 'POST',
      body: new FormData(form)
      })

      const text = await response.text()
      console.log(text)

      const likesPreview = form.querySelector('.post-likes')
      const dislikesPreview = form.querySelector('.post-dislikes')
      const laughsPreview = form.querySelector('.post-laughs')

      // new_stats = await response.json()

      // likesPreview.innerText = new_stats[0]
      // dislikesPreview.innerText = new_stats[1]
      // laughsPreview.innerText = new_stats[2]
    })
  })
}

function postComments() {
  const posts = document.querySelectorAll('.post')
  
  posts.forEach(post => {
    const addForm = post.querySelector('.post .comment-form')
    const textarea = addForm.querySelector('textarea[name="content"]')
    const removeForms = post.querySelectorAll('.delete-comment-form')
    const btn = post.querySelector('.comments-btn') 
    const commentsWrapper = post.querySelector('.comments-wrapper')
    const comments = commentsWrapper.querySelector('.comments')
    const countPreview = post.querySelector('.comments-count')
    
    btn.addEventListener('click', () => {
      btn.classList.toggle('active')
      
      commentsWrapper.classList.toggle('active')
    })

    addForm.addEventListener('submit', async (event) => {
      event.preventDefault()
      if (!textarea.value) {
        textarea.classList.add('invalid')
        return
      }

      const response = await fetch('/posts/comment/new', {
        method: 'POST',
        body: new FormData(addForm)
      }) 
  
      const new_comment = await response.json()
      
      const commentEl = createCommentEl(new_comment['id'], new_comment['username'], new_comment['content'], new_comment['date'], new_comment['user_image'])
      removeFormListeners(commentEl.querySelector('.delete-comment-form'), countPreview)
      
      comments.prepend(commentEl)

      countPreview.innerText++;
    })

    if (removeForms) {
      removeForms.forEach(form => removeFormListeners(form, countPreview))
    }

  })

  function removeFormListeners(removeForm, countPreview) {
    if (removeForm) {
      removeForm.addEventListener('submit', async (event) => {
        event.preventDefault()
  
        const response = await fetch('/posts/comment/delete', {
          method: 'POST',
          body: new FormData(removeForm)
        })
  
        const result = await response.text()

        if (result == 'success') {
          removeForm.closest('.comment').remove()
          countPreview.innerText--;
        }
      })
    }
  }

  function createCommentEl(id, username, content, date, user_image) {
    const commentEl = document.createElement('div')
    commentEl.classList.add('comment', 'd-flex', 'align-items-start', 'gap-2', 'mb-3')
    
    commentEl.innerHTML = 
    `
    <a class="user-image" href="/profile/${username}"><img src="/uploads/${user_image}"></a>
    
    <div class="content border flex-grow-1 rounded px-4">
      <div class="d-flex justify-content-between">
        <p>${username}</p>

        <div class="d-flex gap-1">
          <p>${date.slice(11, 16)}</p>

          <form class="delete-comment-form">
            <input hidden type="hidden" name="comment_id" value="${id}">
            <button type="submit" class="post-btn"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" data-lucide="trash-2" aria-hidden="true" class="lucide lucide-trash-2"><path d="M10 11v6"></path><path d="M14 11v6"></path><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"></path><path d="M3 6h18"></path><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg></button>
          </form>
        </div>
      </div>
    
      <p>${content}</p>
    </div>
    `

    return commentEl
  }
}

function deletePost() {
  const forms = document.querySelectorAll('.post .delete-post-form') 

  forms.forEach(form => {
    form.addEventListener('submit', async (event) => {
      event.preventDefault()

      const response = await fetch('/posts/delete', {
        method: 'POST',
        body: new FormData(form)
      })

      const result = await response.text()
      console.log(result)

      if (result == 'success') {
        form.closest('.post').remove()
      }
    })
  })
}

function Status() {
  const form = document.querySelector('.add-status-form')
  if (!form) return
  const errorPreview = document.querySelector('.status-error-preview')

  form.addEventListener('submit', async (event) => {
    event.preventDefault()

    const input = form.querySelector('input[type="file"]') 

    input.click()
    
    input.addEventListener('change', async () => {

      form.classList.add('loading')
      const response = await fetch('/status/new', {
        method: 'POST',
        body: new FormData(form)
      })
      form.classList.remove('loading')

      const result = await response.text()

      if (result != 'success') {
        errorPreview.textContent = result
      } else {
        window.location.href = '/'
      }
    })
  })
}

function mediaScaling() {
  const medias = document.querySelectorAll('.media')
  const overlay = document.querySelector('.overlay')

  medias.forEach(media => {
    media.addEventListener('click', () => {
      createScaledElement(media)
    })
  })

  function createScaledElement(el) {
    const scaledEl = document.createElement('div')
    scaledEl.classList.add(...el.classList, 'scaled')
    const closeBtn = document.createElement('button')
    closeBtn.classList.add('media-close-btn')
    closeBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-minimize-icon lucide-minimize"><path d="M8 3v3a2 2 0 0 1-2 2H3"/><path d="M21 8h-3a2 2 0 0 1-2-2V3"/><path d="M3 16h3a2 2 0 0 1 2 2v3"/><path d="M16 21v-3a2 2 0 0 1 2-2h3"/></svg>'

    scaledEl.innerHTML = el.innerHTML
    document.body.appendChild(closeBtn)

    document.body.append(scaledEl)
    overlay.classList.add('active')

    closeBtn.addEventListener('click', () => {
      overlay.classList.remove('active')
      scaledEl.remove()
      closeBtn.remove()
    })
    overlay.addEventListener('click', () => {
      overlay.classList.remove('active')
      scaledEl.remove()
      closeBtn.remove()
    })
  }
}

postMediaSelection()
postCategories()
postPublish()
postReactions()
postComments()
deletePost()
Status()
mediaScaling()
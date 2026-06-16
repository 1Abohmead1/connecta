function passwordShowButton() {
  const showBtn = document.querySelector('.show-password-btn')
  const passwordInput = document.querySelector('.showable-password')

  if (!showBtn || !passwordInput) return
  
  showBtn.addEventListener('click', () => {
    showBtn.classList.toggle('active')
 
    if (showBtn.classList.contains('active')) {
      passwordInput.type = 'text'

      showBtn.innerHTML = '<i data-lucide="eye-off"></i>'
      showBtn.setAttribute('title', 'hide password')
    } else {
      passwordInput.type = 'password'

      showBtn.innerHTML = '<i data-lucide="eye"></i>'
      showBtn.setAttribute('title', 'show password')
    }

    lucide.createIcons()
  })
}

function fieldsActivition() {
  const fields = document.querySelectorAll('.field input')
  fields.forEach(field => {
    field.addEventListener('input', () => {
      if (field.value.length > 0) {
        field.classList.add('active')
      } else if (field.type != 'date') {
        field.classList.remove('active')
      }
    })
  })
}

function fieldsValidation() {
  const loginForm = document.querySelector('.login-form')
  if (!loginForm) return
  const submitBtn = loginForm.querySelector('.auth-btn')
  if (!submitBtn) return
  const fields = document.querySelectorAll('.field-section.required')
  if (!fields) return
  let hasError = false

  loginForm.addEventListener('submit', async (event) => {
    event.preventDefault()
    
    fields.forEach(field => {
      const input = field.querySelector('input')
      const errorsPreview = field.querySelector('.error-preview')
      if (!input.value) {
        const error = `${input.name.replaceAll('_', ' ')} is required!`

        newError(error, errorsPreview, input)
        hasError = true
      }
    })
    
    errorsCheck()

    if (!hasError) {
      
      if (!submitBtn.classList.contains('loading')) {
        submitBtn.classList.add('loading')
      }
      
      await getResult()
      if (submitBtn.classList.contains('loading')) {
        submitBtn.classList.remove('loading')
      }
      
      async function getResult() {
        const formData = new FormData(loginForm)
        const path = window.location.pathname

        const response = await fetch(path, {
          method: 'POST',
          body: formData
        })

        const result = await response.text()

        if (result != 'success') {
          let errorFieldFound = false
          fields.forEach(field => {
            const input = field.querySelector('input')
            const errorsPreview = field.querySelector('.error-preview')

            hasError = true
            submitBtn.disabled = hasError
            
            if (result.includes(input.name)) {
              newError(result, errorsPreview, input)
              errorFieldFound = true
            }
          })

          if (!errorFieldFound) {
            const gloabalErrorPreview = document.querySelector('.global-error-preview')
            newError(result, gloabalErrorPreview)
          }
        } else {
          window.location.href= '/'
        }
      }
    }
  })
  
  fields.forEach(field => {
    const input = field.querySelector('input')
    const errorsPreview = field.querySelector('.error-preview')
    
    input.addEventListener('input', () => {
      hasError = false

      if (!input.value) {
        const error = `${input.name.replaceAll('_', ' ')} is required!`
        errorsPreview.innerHTML = ''
        
        hasError = true
        newError(error, errorsPreview, input)
      } else {
        resetInput(input, errorsPreview)
      }
      
      errorsCheck()
    })

    if (input.type == 'date') {
      input.addEventListener('change', () => {
        const year = Number(input.value.split('-')[0])
        const month = Number(input.value.split('-')[1])
        const day = Number(input.value.split('-')[2])
  
        current_year = new Date().getFullYear()
        if (year > current_year || year < 1900 || current_year - year < 12) {
          newError("invalid year!", errorsPreview, input)
        }
        if (month > 12) {
          newError("invalid month!", errorsPreview, input)
        }
      })
    }
  })
  
  function errorsCheck() {
    fields.forEach(field => {
      const errors = field.querySelectorAll('.error-preview .error')
      
      if (errors.length > 0) {
        hasError = true 
      }
    })

    submitBtn.disabled = hasError
  }
}

function newError(error, errorsPreview, input) {
  const errorEl = document.createElement('p')
  errorEl.classList.add('error', 'text-danger', 'fw-bold', 'fs-6')
  errorEl.innerText = error
  
  const errors = [...errorsPreview.querySelectorAll('.error')].map(error => error.innerText)
  if (!errors.includes(error)) {
    errorsPreview.appendChild(errorEl)
    if (input) {
      input.classList.add('invalid')
    }
  }
}

function resetInput(input, errorsPreview) {
  input.classList.remove('invalid')
  errorsPreview.innerHTML = ''
}

passwordShowButton()
fieldsActivition()
fieldsValidation()
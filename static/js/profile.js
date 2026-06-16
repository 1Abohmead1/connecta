function friendRequest() {
  const form = document.querySelector('.friend-request-form');
  if (!form) return;
  const btn = document.querySelector('.friend-request-btn');

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (btn.classList.contains('active')) return;

    btn.classList.add('active');
    btn.innerHTML = 'friend request sent';
    btn.disabled = true;

    await fetch('/friends/request', {
      method: 'POST',
      body: new FormData(form)
    });
  });
}

function updateProfile() {
  const form = document.querySelector('.update-form')
  const errorPreview = form.querySelector('.error-preview')

  form.addEventListener('submit', async (event) => {
    event.preventDefault()

    const response = await fetch('/profile/update', {
      method: 'POST',
      body: new FormData(form)
    })

    const result = await response.text()

    if (result != 'success') {
      errorPreview.textContent = result
    } else {
      window.location.href = '/profile/'
    }
  })
}

friendRequest()
updateProfile()
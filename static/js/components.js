function logo() {
  const logoContainer = document.querySelector('logoContainer')
  if (!logoContainer) return
  const logo = document.createElement('logo')
  const logoIcon = document.createElement('i')
  
  logoIcon.setAttribute('data-lucide', 'zap')
  logo.appendChild(logoIcon)
  logoContainer.appendChild(logo)
  
  const color = logoContainer.getAttribute('data-brand') 
  const brandName = document.createElement('a')
  if (color) {
    brandName.style.color = color
  }
  
  brandName.href = '/'
  brandName.innerText = 'Connecta'
  logoContainer.appendChild(brandName)
}

function uploadBtn() {
  const btns = document.querySelectorAll('.upload-btn')
  if (!btns) return
  
  btns.forEach(btn => {
    const input = btn.querySelector('input[type="file"]')
    btn.addEventListener('click', () => {
      input.focus()
      input.click()
    })
  })
}


logo()
uploadBtn()
lucide.createIcons()
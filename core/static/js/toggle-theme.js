function toggleTheme() {

    const htmlTag = document.getElementsByTagName('html')[0]
    const buttonIcon = document.getElementById("toggle-icon")

    if (htmlTag.hasAttribute('data-theme')) {
      htmlTag.removeAttribute('data-theme')
      buttonIcon.className = 'fas fa-sun'
      return window.localStorage.removeItem('site-theme')
    }

    htmlTag.setAttribute('data-theme', 'light')
    buttonIcon.className = 'fas fa-moon'
    window.localStorage.setItem('site-theme', 'light')
    


  }

  function applyInitialTheme() {
    const theme = window.localStorage.getItem('site-theme')
    if (theme !== null) {
      const htmlTag = document.getElementsByTagName('html')[0]
      const buttonIcon = document.getElementById("toggle-icon")
      
      htmlTag.setAttribute('data-theme', theme)
      buttonIcon.className = 'fas fa-moon'
      
    }
    
  }

  applyInitialTheme()

  document
    .getElementById('theme-toggle')
    .addEventListener('click', toggleTheme)
document.getElementById('login-form').addEventListener('submit', function(e) {
  e.preventDefault();

  const formData = new FormData(this);

  const nextInput = document.querySelector('input[name="next"]');
  if (nextInput) {
    formData.append('next', nextInput.value);
  }

  fetch('/login/', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    if (data.errors) {
      const errorMessages = document.getElementById('error-messages');
      errorMessages.innerHTML = '';

      data.errors.forEach(error => {
        const p = document.createElement('p');
        p.textContent = error;
        errorMessages.appendChild(p);
      });

      const modal = new bootstrap.Modal(document.getElementById('loginErrorModal'));
      modal.show();
    } else {
      window.location.href = data.next || '/';
    }
  })
  .catch(error => console.error('Ошибка:', error));
});

const profileLink = document.getElementById('profileLink');
const sidebar = document.getElementById('sidebar');
const closeSidebar = document.getElementById('closeSidebar');
const overlay = document.getElementById('overlay');

if (profileLink) {
    profileLink.addEventListener('click', function(e) {
        e.preventDefault();
        sidebar.classList.add('open');
        overlay.classList.add('show');
    });
}

if (closeSidebar) {
    closeSidebar.addEventListener('click', function() {
        sidebar.classList.remove('open');
        overlay.classList.remove('show');
    });
}

overlay.addEventListener('click', function() {
    sidebar.classList.remove('open');
    overlay.classList.remove('show');
});

document.getElementById('burgerMenu').addEventListener('click', function (event) {
    let menu = document.getElementById('mobileNav');
    menu.style.display = (menu.style.display === 'block') ? 'none' : 'block';
    event.stopPropagation();
});

document.addEventListener('click', function (event) {
    let menu = document.getElementById('mobileNav');
    let burger = document.getElementById('burgerMenu');

    if (menu.style.display === 'block' && !menu.contains(event.target) && !burger.contains(event.target)) {
        menu.style.display = 'none';
    }
});
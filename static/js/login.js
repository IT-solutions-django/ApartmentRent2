document.getElementById('login-form').addEventListener('submit', function(e) {
  e.preventDefault();

  const formData = new FormData(this);

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
      window.location.href = '/';
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
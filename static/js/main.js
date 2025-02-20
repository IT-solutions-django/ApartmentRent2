const prevButton = document.getElementById('prevReview');
const nextButton = document.getElementById('nextReview');
const reviewsContainer = document.getElementById('reviewsContainer');
const reviews = Array.from(reviewsContainer.getElementsByClassName('review-card'));
let currentIndex = 0;

function updateReviews() {
    const visibleReviews = reviews.slice(currentIndex, currentIndex + 3);
    reviewsContainer.innerHTML = '';
    visibleReviews.forEach(review => reviewsContainer.appendChild(review));
}

prevButton.addEventListener('click', () => {
    if (currentIndex > 0) {
        currentIndex -= 3;
        updateReviews();
    }
});

nextButton.addEventListener('click', () => {
    if (currentIndex + 3 < reviews.length) {
        currentIndex += 3;
        updateReviews();
    }
});

updateReviews();

document.addEventListener("DOMContentLoaded", function() {
    // Получаем все ссылки пагинации
    const paginationLinks = document.querySelectorAll('.pagination a');

    // Проверяем текущую активную страницу через URL
    const currentPage = window.location.search.match(/page=(\d+)/);

    if (currentPage) {
        const activePage = currentPage[1];  // Номер активной страницы
        paginationLinks.forEach(link => {
            // Если это активная страница, добавляем стиль
            if (link.href.includes(`?page=${activePage}`)) {
                link.classList.add('active-page');
            } else {
                link.classList.remove('active-page');
            }
        });
    }
});

const profileLink = document.getElementById('profileLink');
const profileLink2 = document.getElementById('profileLink2');
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

if (profileLink2) {
    profileLink2.addEventListener('click', function(e) {
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

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('feedback-form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = new FormData(form);
        const cardId = form.dataset.cardId;

        fetch('/', {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('modalMessage').textContent = data.error;
                const modal = new bootstrap.Modal(document.getElementById('loginErrorModal'));
                modal.show();
            } else if (data.success) {
                document.getElementById('modalMessage').textContent = data.success;

                const modal = new bootstrap.Modal(document.getElementById('loginErrorModal'));
                modal.show();

                form.reset();
            }
        })
        .catch(error => {
            console.error('Ошибка при отправке запроса:', error);
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
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



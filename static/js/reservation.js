document.addEventListener("DOMContentLoaded", function() {
    const checkInInput = document.getElementById("check-in-date");
    const checkOutInput = document.getElementById("check-out-date");
    const daysCountSpan = document.getElementById("days-count");
    const priceElement = document.getElementById('total-price');
    const priceSpan = parseFloat(priceElement.dataset.defaultPrice);



    function calculatePrice(count_days) {
        if (!isNaN(priceSpan)) {
            const total_price = priceSpan * count_days;
            priceElement.textContent = total_price + " ₽";
        }
    }

    function calculateDays() {
        const checkInDate = new Date(checkInInput.value);
        const checkOutDate = new Date(checkOutInput.value);

        if (!isNaN(checkInDate) && !isNaN(checkOutDate) && checkOutDate > checkInDate) {
            const timeDiff = checkOutDate - checkInDate;
            const days = Math.ceil(timeDiff / (1000 * 60 * 60 * 24));
            daysCountSpan.textContent = days + ' сутки';
            calculatePrice(days);
        } else {
            daysCountSpan.textContent = 0;
        }
    }

    checkInInput.addEventListener("change", calculateDays);
    checkOutInput.addEventListener("change", calculateDays);

    calculateDays();
});

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('booking-form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = new FormData(form);
        const cardId = form.dataset.cardId;

        fetch(`/reservation/${cardId}/`, {
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

                setTimeout(function() {
                    window.location.href = data.redirect_url;
                }, 1500);
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
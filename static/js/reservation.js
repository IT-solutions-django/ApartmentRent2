document.addEventListener("DOMContentLoaded", function() {
    const checkInInput = document.getElementById("check-in-date");
    const checkOutInput = document.getElementById("check-out-date");
    const daysCountSpan = document.getElementById("days-count");

    function calculateDays() {
        const checkInDate = new Date(checkInInput.value);
        const checkOutDate = new Date(checkOutInput.value);

        if (!isNaN(checkInDate) && !isNaN(checkOutDate) && checkOutDate > checkInDate) {
            const timeDiff = checkOutDate - checkInDate;
            const days = Math.ceil(timeDiff / (1000 * 60 * 60 * 24));
            daysCountSpan.textContent = days + ' сутки';
        } else {
            daysCountSpan.textContent = 0;
        }
    }

    checkInInput.addEventListener("change", calculateDays);
    checkOutInput.addEventListener("change", calculateDays);
});
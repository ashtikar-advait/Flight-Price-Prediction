document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const departureTimeInput = document.querySelector('input[name="Dep_Time"]');
    const arrivalTimeInput = document.querySelector('input[name="Arrival_Time"]');

    form.addEventListener('submit', function(event) {
        // Validate departure and arrival times
        const departureTime = new Date(departureTimeInput.value);
        const arrivalTime = new Date(arrivalTimeInput.value);

        if (departureTime >= arrivalTime) {
            event.preventDefault();
            alert('Arrival time must be later than departure time.');
        }
    });

    // Optional: Prevent selecting past dates
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');

    const minDateTime = `${year}-${month}-${day}T${hours}:${minutes}`;
    departureTimeInput.setAttribute('min', minDateTime);
    arrivalTimeInput.setAttribute('min', minDateTime);
});

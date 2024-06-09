document.getElementById('booking-form').addEventListener('submit', function(event) {
    const date = document.getElementById('date').value;
    const time = document.getElementById('time').value;

    // Basic validation example
    if (!date || !time) {
        alert('Please fill out all required fields.');
        event.preventDefault();
        return;
    }

    // Proceed with form submission
    const formData = new FormData(event.target);
    const data = {
        name: formData.get('name'),
        contact: formData.get('contact'),
        service: formData.get('service'),
        date: formData.get('date'),
        time: formData.get('time'),
        notes: formData.get('notes')
    };

    console.log('Booking Data:', data);

    alert('Your appointment has been booked successfully!');
});

document.getElementById('booking-form').addEventListener('submit', function(event) {
    event.preventDefault();

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


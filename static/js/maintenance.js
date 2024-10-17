document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('maintenanceForm');
    if (form) {
        form.addEventListener('submit', function(event) {
            if (!validateForm()) {
                event.preventDefault();
            }
        });
    }
});

function validateForm() {
    const date = document.getElementById('date').value;
    const lot = document.getElementById('lot').value;
    const details = document.getElementById('details').value;

    if (!date || !lot || !details) {
        alert('Please fill in all fields');
        return false;
    }

    return true;
}

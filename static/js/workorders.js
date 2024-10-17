document.addEventListener('DOMContentLoaded', function() {
    const statusFilters = document.querySelectorAll('.status-filter');
    statusFilters.forEach(filter => {
        filter.addEventListener('change', filterWorkOrders);
    });
});

function filterWorkOrders() {
    const selectedStatuses = Array.from(document.querySelectorAll('.status-filter:checked'))
        .map(checkbox => checkbox.value);

    const workOrders = document.querySelectorAll('.work-order');
    workOrders.forEach(order => {
        const status = order.getAttribute('data-status');
        if (selectedStatuses.length === 0 || selectedStatuses.includes(status)) {
            order.style.display = '';
        } else {
            order.style.display = 'none';
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    var socket = io('/notifications');

    socket.on('connect', function() {
        console.log('Connected to notifications namespace');
    });

    socket.on('notification', function(data) {
        console.log('Received notification:', data);
        showNotification(data.message, data.category, data.data);
    });

    function showNotification(message, category, data) {
        console.log('Showing notification:', message, category, data);
        var notificationArea = document.getElementById('notification-area');
        if (!notificationArea) {
            notificationArea = document.createElement('div');
            notificationArea.id = 'notification-area';
            notificationArea.style.position = 'fixed';
            notificationArea.style.top = '20px';
            notificationArea.style.right = '20px';
            notificationArea.style.zIndex = '1000';
            document.body.appendChild(notificationArea);
        }

        var notification = document.createElement('div');
        notification.className = `alert alert-${category} alert-dismissible fade show`;
        notification.role = 'alert';
        
        var content = `
            <strong>${message}</strong>
            ${data ? `<br>${data.description}<br>Priority: ${data.priority}` : ''}
            ${data && data.url ? `<br><a href="${data.url}" class="alert-link">View Work Order</a>` : ''}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        notification.innerHTML = content;

        notificationArea.appendChild(notification);

        // For urgent notifications, add a sound alert
        if (category === 'danger') {
            playAlertSound();
        }

        // Remove the notification after 10 seconds for normal notifications, 30 seconds for urgent ones
        setTimeout(function() {
            notification.remove();
        }, category === 'danger' ? 30000 : 10000);
    }

    function playAlertSound() {
        var audio = new Audio('/static/sounds/urgent_alert.mp3');
        audio.play();
    }
});

document.addEventListener('DOMContentLoaded', function() {
    fetchChartData();
});

function fetchChartData() {
    fetch('/api/chart_data')
        .then(response => response.json())
        .then(data => {
            createTaskChart(data.task_stats);
            createWorkOrderChart(data.work_order_stats);
            createMaintenanceChart(data.maintenance_stats);
        });
}

function createTaskChart(taskStats) {
    const ctx = document.getElementById('taskChart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: Object.keys(taskStats),
            datasets: [{
                data: Object.values(taskStats),
                backgroundColor: ['#007bff', '#ffc107', '#28a745'],
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Task Status Distribution'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function createWorkOrderChart(workOrderStats) {
    const ctx = document.getElementById('workOrderChart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: Object.keys(workOrderStats),
            datasets: [{
                data: Object.values(workOrderStats),
                backgroundColor: ['#007bff', '#ffc107', '#28a745'],
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Work Order Status Distribution'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function createMaintenanceChart(maintenanceStats) {
    const ctx = document.getElementById('maintenanceChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: Object.keys(maintenanceStats),
            datasets: [{
                label: 'Maintenance Logs',
                data: Object.values(maintenanceStats),
                borderColor: '#007bff',
                fill: false
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Maintenance Logs Over Time'
                }
            },
            scales: {
                x: {
                    type: 'category',
                    title: {
                        display: true,
                        text: 'Month'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Logs'
                    },
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
}

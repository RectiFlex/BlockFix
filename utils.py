from models import WorkOrder, db
from app import socketio
from flask import url_for
import logging
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_work_order(maintenance_log):
    is_urgent = "urgent" in maintenance_log.details.lower() or "immediate attention" in maintenance_log.details.lower()
    priority = "Urgent" if is_urgent else "Normal"

    work_order = WorkOrder(
        title=f"{'Urgent: ' if is_urgent else ''}Maintenance required for Lot {maintenance_log.lot}",
        description=f"Based on maintenance log: {maintenance_log.details}",
        status="Pending",
        priority=priority,
        created_by=maintenance_log.user_id
    )
    db.session.add(work_order)
    db.session.commit()

    logger.info(f"Work order created: {work_order.id}, Is urgent: {is_urgent}")

    send_notification(
        work_order.title,
        'danger' if is_urgent else 'info',
        {
            'id': work_order.id,
            'description': work_order.description,
            'priority': work_order.priority,
            'url': url_for('view_workorder', id=work_order.id)
        }
    )

def send_notification(message, category, data=None):
    logger.info(f"Sending notification: {message}, Category: {category}, Data: {data}")
    socketio.emit('notification', {
        'message': message,
        'category': category,
        'data': data
    }, namespace='/notifications')
    logger.info("Notification sent")

def send_urgent_notification(work_order):
    send_notification(
        f"Urgent: New work order for Lot {work_order.maintenance_log.lot}",
        'danger',
        {
            'id': work_order.id,
            'description': work_order.description,
            'priority': work_order.priority,
            'url': url_for('view_workorder', id=work_order.id)
        }
    )

def generate_work_order_pdf(work_order):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    p.setTitle(f"Work Order - {work_order.title}")
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, f"Work Order - {work_order.title}")

    p.setFont("Helvetica", 12)
    details = [
        f"ID: {work_order.id}",
        f"Status: {work_order.status}",
        f"Priority: {work_order.priority}",
        f"Due Date: {work_order.due_date.strftime('%Y-%m-%d') if work_order.due_date else 'Not set'}",
        f"Created: {work_order.created_at.strftime('%Y-%m-%d %H:%M')}",
        f"Last Updated: {work_order.updated_at.strftime('%Y-%m-%d %H:%M')}",
        f"Assigned To: {work_order.user.username if work_order.user else 'Unassigned'}",
        f"Created By: {work_order.creator.username if work_order.creator else 'Unknown'}",
    ]

    y = height - 80
    for detail in details:
        p.drawString(50, y, detail)
        y -= 20

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y - 20, "Description:")
    p.setFont("Helvetica", 12)
    description_lines = [work_order.description[i:i+80] for i in range(0, len(work_order.description), 80)]
    for line in description_lines:
        y -= 20
        p.drawString(50, y, line)

    y -= 40
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Task:")
    p.setFont("Helvetica", 12)
    task_lines = [work_order.task[i:i+80] for i in range(0, len(work_order.task), 80)]
    for line in task_lines:
        y -= 20
        p.drawString(50, y, line)

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), default='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class MaintenanceLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    lot = db.Column(db.String(64))
    details = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class WorkOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='Pending')
    priority = db.Column(db.String(20), default='Normal')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    due_date = db.Column(db.DateTime, nullable=True)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    maintenance_log_id = db.Column(db.Integer, db.ForeignKey('maintenance_log.id'))
    task = db.Column(db.Text)  # New field for task description

    user = db.relationship('User', foreign_keys=[assigned_to], backref='assigned_work_orders')
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_work_orders')
    maintenance_log = db.relationship('MaintenanceLog', backref='work_orders')

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    description = db.Column(db.Text)
    status = db.Column(db.String(20))
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    work_order_id = db.Column(db.Integer, db.ForeignKey('work_order.id'))

    work_order = db.relationship('WorkOrder', backref='tasks')

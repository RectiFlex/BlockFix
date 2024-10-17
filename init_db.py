from app import app, db
from models import User

def create_admin_user():
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@example.com', role='admin')
        admin.set_password('admin')  # Set a default password
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully.")
    else:
        print("Admin user already exists.")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_admin_user()

"""
Script to create a default admin user.
"""
from app import create_app
from app.models import db, User
from werkzeug.security import generate_password_hash
import logging

# Create Flask app
app = create_app()
logger = logging.getLogger(__name__)

def create_admin():
    """
    Create an admin account if it doesn't already exist.
    """
    admin_phone = '0000000'
    admin_password = generate_password_hash('admin', method="pbkdf2:sha256")
    admin_fullname = 'Administrator'
    
    try:
        # Check if admin is already registered
        existing_admin = User.query.filter_by(phone_number=admin_phone).first()
        if existing_admin:
            print('Administrator account already exists.')
            return existing_admin
        else:
            new_admin = User(
                fullname=admin_fullname, 
                phone_number=admin_phone, 
                password=admin_password,
                is_admin=True
            )
            db.session.add(new_admin)
            db.session.commit()
            print(f'Administrator account created successfully with ID: {new_admin.id}')
            return new_admin
    except Exception as e:
        print(f'Error creating administrator account: {str(e)}')
        return None

if __name__ == '__main__':
    with app.app_context():
        admin = create_admin()
        if admin:
            print(f'Admin user: {admin.fullname}, Phone: {admin.phone_number}')

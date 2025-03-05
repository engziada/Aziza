from app import create_app
from app.models import db, User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Check if admin exists
    admin = User.query.filter_by(phone_number='0000000').first()
    print(f'Admin exists: {admin is not None}')
    
    # Delete existing admin if it exists
    if admin:
        db.session.delete(admin)
        db.session.commit()
        print('Deleted existing admin')
    
    # Create new admin
    admin_phone = '0000000'
    admin_password = generate_password_hash('admin', method="pbkdf2:sha256")
    admin_fullname = 'Administrator'
    
    new_admin = User(
        fullname=admin_fullname, 
        phone_number=admin_phone, 
        password=admin_password,
        is_admin=True
    )
    db.session.add(new_admin)
    db.session.commit()
    print('Created new admin')
    
    # Verify admin was created with correct password
    admin = User.query.filter_by(phone_number='0000000').first()
    if admin:
        print(f'Admin ID: {admin.id}')
        print(f'Admin name: {admin.fullname}')
        print(f'Admin phone: {admin.phone_number}')
        print(f'Admin is_admin: {admin.is_admin}')
        from werkzeug.security import check_password_hash
        print(f'Password check result: {check_password_hash(admin.password, "admin")}')

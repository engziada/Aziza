from app import app, db, User, create_admin

with app.app_context():
    # Check if admin exists
    admin = User.query.filter_by(phoneno='0000000').first()
    print(f'Admin exists: {admin is not None}')
    
    # Delete existing admin if it exists
    if admin:
        db.session.delete(admin)
        db.session.commit()
        print('Deleted existing admin')
    
    # Create new admin
    create_admin()
    print('Created new admin')
    
    # Verify admin was created with correct password
    admin = User.query.filter_by(phoneno='0000000').first()
    if admin:
        print(f'Admin password hash: {admin.password}')
        print(f'Password check result: {admin.check_password("admin")}')

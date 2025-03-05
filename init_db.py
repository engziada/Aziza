from app import create_app
from app.models import db, User, MaritalStatus
from werkzeug.security import generate_password_hash

def init_db():
    """Initialize the database with required data."""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if admin user exists
        admin = User.query.filter_by(is_admin=True).first()
        if not admin:
            # Create admin user
            admin = User(
                fullname='Admin',
                phone_number='123456789',
                is_admin=True,
                password=generate_password_hash('admin123')
            )
            db.session.add(admin)
        
        # Add marital statuses if they don't exist
        statuses = [
            'Single',
            'Married',
            'Divorced',
            'Widowed'
        ]
        
        for status in statuses:
            existing = MaritalStatus.query.filter_by(status_name=status).first()
            if not existing:
                db.session.add(MaritalStatus(status_name=status))
        
        # Commit changes
        db.session.commit()
        
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()

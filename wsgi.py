import os
import logging
from app import create_app
from app.models import db, User, MaritalStatus
from werkzeug.security import generate_password_hash

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get configuration from environment or use default
config_name = os.environ.get('FLASK_CONFIG', 'production')
app = create_app(config_name)

# Initialize the database when the app starts
with app.app_context():
    try:
        # Create all tables
        db.create_all()
        logger.info("Database tables created successfully")
        
        # Check if admin user exists
        admin = User.query.filter_by(phone_number='0000000').first()
        if not admin:
            # Create admin user
            admin = User(
                fullname='Administrator',
                phone_number='0000000',
                password=generate_password_hash('admin', method="pbkdf2:sha256"),
                is_admin=True
            )
            db.session.add(admin)
            logger.info("Admin user created")
        
        # Add marital statuses if they don't exist
        statuses = [
            'أعزب',
            'متزوج',
            'مطلق',
            'أرمل'
        ]
        
        for status in statuses:
            existing = MaritalStatus.query.filter_by(status_name=status).first()
            if not existing:
                db.session.add(MaritalStatus(status_name=status))
                logger.info(f"Added marital status: {status}")
        
        # Commit changes
        db.session.commit()
        logger.info("Database initialized successfully!")
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error initializing database: {str(e)}")

if __name__ == '__main__':
    app.run()
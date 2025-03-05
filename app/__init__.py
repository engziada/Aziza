from flask import Flask
from flask_migrate import Migrate
from app.models import db
from config import config
from app.utils import setup_logging
import os
import logging

# Initialize extensions
migrate = Migrate()
logger = logging.getLogger(__name__)

def create_admin_user(app):
    """
    Create an admin user if one doesn't exist.
    """
    from app.models import User
    from werkzeug.security import generate_password_hash
    
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(phone_number='0000000').first()
        if admin:
            logger.info("Admin user already exists.")
            return
        
        # Create admin user
        try:
            admin = User(
                fullname='Administrator',
                phone_number='0000000',
                password=generate_password_hash('admin', method="pbkdf2:sha256"),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            logger.info("Admin user created successfully.")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating admin user: {str(e)}")

def create_app(config_name='default'):
    """
    Application factory function.
    
    Args:
        config_name (str): Configuration to use (default, development, production, testing)
        
    Returns:
        Flask application instance
    """
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Ensure the Logs directory exists
    if not os.path.exists(app.config.get('LOG_DIR', 'Logs')):
        os.makedirs(app.config.get('LOG_DIR', 'Logs'))
    
    # Set up logging
    setup_logging(app)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.auth import auth_bp
    from app.profile import profile_bp
    from app.admin import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(admin_bp)
    
    # Create admin user if it doesn't exist
    create_admin_user(app)
    
    return app
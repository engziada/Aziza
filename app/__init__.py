from flask import Flask
from flask_migrate import Migrate
from app.models import db
from config import config
from app.utils import setup_logging
import os

# Initialize extensions
migrate = Migrate()

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
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    
    return app
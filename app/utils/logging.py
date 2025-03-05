import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

def setup_logging(app):
    """
    Set up logging for the application.
    
    Args:
        app: Flask application instance
    """
    log_dir = app.config.get('LOG_DIR', 'Logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create a unique log file for each run
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(log_dir, f'app_{timestamp}.log')
    
    # Set up file handler with rotation (max 10MB per file, keep 10 backup files)
    file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    
    # Set up console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    console_handler.setLevel(logging.INFO)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Configure app logger
    app.logger.setLevel(logging.INFO)
    
    # Log application startup
    app.logger.info(f"Starting application in {app.config.get('ENV', 'development')} mode")

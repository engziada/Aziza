import os
from app import create_app
from app.models import db

# Get configuration from environment or use default
config_name = os.environ.get('FLASK_CONFIG', 'production')
app = create_app(config_name)

# Initialize the database when the app starts
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
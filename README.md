# Marriage Matchmaking System

A Flask-based web application for marriage matchmaking services.

## Features

- User authentication (login, registration, password reset)
- Profile creation and management
- Search for potential matches based on criteria
- Admin dashboard for user management
- Secure password handling
- WhatsApp notifications for match requests

## Project Structure

```
Marriage-Matchmaking-System/
├── app/                        # Main application package
│   ├── __init__.py             # Application factory
│   ├── auth/                   # Authentication module
│   │   ├── __init__.py
│   │   └── routes.py           # Authentication routes
│   ├── profile/                # Profile module
│   │   ├── __init__.py
│   │   └── routes.py           # Profile routes
│   ├── admin/                  # Admin module
│   │   ├── __init__.py
│   │   └── routes.py           # Admin routes
│   ├── models/                 # Database models
│   │   ├── __init__.py
│   │   └── models.py           # SQLAlchemy models
│   ├── services/               # Business logic services
│   │   ├── __init__.py
│   │   ├── auth_service.py     # Authentication service
│   │   ├── profile_service.py  # Profile service
│   │   ├── request_service.py  # Match request service
│   │   └── admin_service.py    # Admin service
│   ├── utils/                  # Utility functions
│   │   ├── __init__.py
│   │   ├── password.py         # Password utilities
│   │   ├── notifications.py    # Notification utilities
│   │   └── logging.py          # Logging utilities
│   ├── static/                 # Static files (CSS, JS, images)
│   └── templates/              # Jinja2 templates
├── migrations/                 # Database migrations
├── Logs/                       # Application logs
├── config.py                   # Configuration settings
├── init_db.py                  # Database initialization script
├── run.py                      # Application entry point
├── copy_assets.py              # Script to copy templates and static files
└── requirements.txt            # Project dependencies
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Marriage-Matchmaking-System.git
cd Marriage-Matchmaking-System
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python init_db.py
```

5. Run the application:
```bash
python run.py
```

6. Access the application at http://localhost:5050

## Checkpoints

### Checkpoint 1 - 2025-03-05
- Restructured project to follow Flask application factory pattern
- Created modular architecture with blueprints for auth and profile
- Implemented service layer for business logic
- Added database models with improved naming conventions
- Set up logging system
- Added database migration support
- Created configuration management system

To revert to this checkpoint:
```bash
git checkout checkpoint-1
from app.models import User

def check_password(username: str, password: str) -> int:
    """
    Check if the username and password match a user in the database.
    
    Args:
        username (str): The username (phone number)
        password (str): The password to check
        
    Returns:
        int: 0 if successful, -1 if password is incorrect, -2 if user doesn't exist
    """
    phone_number = username
    user = User.query.filter_by(phone_number=phone_number).first()
    
    # If account exists
    if user:
        # Check for password using the model's method
        if user.check_password(password):
            return 0
        else:
            return -1
    else:
        return -2

def update_password(username: str, password: str) -> bool:
    """
    Update a user's password.
    
    Args:
        username (str): The username (phone number)
        password (str): The new password
        
    Returns:
        bool: True if successful, False otherwise
    """
    user = User.query.filter_by(phone_number=username).first()
    if user:
        user.set_password(password)
        from app.models import db
        db.session.commit()
        return True
    return False

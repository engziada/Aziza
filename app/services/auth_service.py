from app.models import db, User
from app.utils import send_whatsapp_notification
import logging
import random
import string

logger = logging.getLogger(__name__)

class AuthService:
    """Service class for authentication-related operations."""
    
    @staticmethod
    def login(phone_number, password):
        """
        Authenticate a user.
        
        Args:
            phone_number (str): User's phone number
            password (str): User's password
            
        Returns:
            tuple: (User object, error message)
        """
        user = User.query.filter_by(phone_number=phone_number).first()
        
        if not user:
            logger.info(f"Login attempt with non-existent phone number: {phone_number}")
            return None, "User does not exist"
            
        if not user.check_password(password):
            logger.warning(f"Failed login attempt for user: {phone_number}")
            return None, "Incorrect password"
            
        logger.info(f"Successful login for user: {phone_number}")
        return user, None
    
    @staticmethod
    def register(fullname, phone_number, password):
        """
        Register a new user.
        
        Args:
            fullname (str): User's full name
            phone_number (str): User's phone number
            password (str): User's password
            
        Returns:
            tuple: (User object, error message)
        """
        # Check if user already exists
        existing_user = User.query.filter_by(phone_number=phone_number).first()
        if existing_user:
            logger.info(f"Registration attempt with existing phone number: {phone_number}")
            return None, "User with this phone number already exists"
        
        # Create new user
        user = User(fullname=fullname, phone_number=phone_number)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            logger.info(f"New user registered: {phone_number}")
            return user, None
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error registering user: {str(e)}")
            return None, f"Error registering user: {str(e)}"
    
    @staticmethod
    def reset_password(phone_number):
        """
        Reset a user's password and send the new password via WhatsApp.
        
        Args:
            phone_number (str): User's phone number
            
        Returns:
            tuple: (success boolean, message)
        """
        user = User.query.filter_by(phone_number=phone_number).first()
        
        if not user:
            logger.info(f"Password reset attempt for non-existent user: {phone_number}")
            return False, "User does not exist"
        
        # Generate a random password
        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        
        # Update the user's password
        user.set_password(new_password)
        
        try:
            db.session.commit()
            
            # Send the new password via WhatsApp
            message = f"Your new password is: {new_password}"
            send_whatsapp_notification(phone_number, message)
            
            logger.info(f"Password reset for user: {phone_number}")
            return True, "Password reset successful. Check your WhatsApp for the new password."
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error resetting password: {str(e)}")
            return False, f"Error resetting password: {str(e)}"
    
    @staticmethod
    def change_password(user_id, current_password, new_password):
        """
        Change a user's password.
        
        Args:
            user_id (int): User's ID
            current_password (str): User's current password
            new_password (str): User's new password
            
        Returns:
            tuple: (success boolean, message)
        """
        user = User.query.get(user_id)
        
        if not user:
            logger.warning(f"Password change attempt for non-existent user ID: {user_id}")
            return False, "User does not exist"
        
        if not user.check_password(current_password):
            logger.warning(f"Password change attempt with incorrect current password for user ID: {user_id}")
            return False, "Current password is incorrect"
        
        user.set_password(new_password)
        
        try:
            db.session.commit()
            logger.info(f"Password changed for user ID: {user_id}")
            return True, "Password changed successfully"
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error changing password: {str(e)}")
            return False, f"Error changing password: {str(e)}"

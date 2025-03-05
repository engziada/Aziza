from app.models import db, User, Profile, Request, MaritalStatus
import pandas as pd
import io
import logging

logger = logging.getLogger(__name__)

class AdminService:
    """Service class for administrative operations."""
    
    @staticmethod
    def create_admin(fullname, phone_number, password):
        """
        Create an admin user.
        
        Args:
            fullname (str): Admin's full name
            phone_number (str): Admin's phone number
            password (str): Admin's password
            
        Returns:
            tuple: (User object, error message)
        """
        # Check if user already exists
        existing_user = User.query.filter_by(phone_number=phone_number).first()
        if existing_user:
            logger.info(f"Admin creation attempt with existing phone number: {phone_number}")
            return None, "User with this phone number already exists"
        
        # Create new admin user
        user = User(fullname=fullname, phone_number=phone_number, is_admin=True)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            logger.info(f"New admin user created: {phone_number}")
            return user, None
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating admin user: {str(e)}")
            return None, f"Error creating admin user: {str(e)}"
    
    @staticmethod
    def get_all_users():
        """
        Get all users.
        
        Returns:
            list: List of all users
        """
        return User.query.all()
    
    @staticmethod
    def delete_user(user_id):
        """
        Delete a user and all associated data.
        
        Args:
            user_id (int): User's ID
            
        Returns:
            tuple: (success boolean, message)
        """
        user = User.query.get(user_id)
        
        if not user:
            logger.warning(f"User deletion attempt for non-existent user ID: {user_id}")
            return False, "User does not exist"
        
        try:
            # Delete user (cascading delete will handle associated profiles and requests)
            db.session.delete(user)
            db.session.commit()
            
            logger.info(f"User deleted: ID {user_id}")
            return True, "User deleted successfully"
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting user: {str(e)}")
            return False, f"Error deleting user: {str(e)}"
    
    @staticmethod
    def approve_request(request_id):
        """
        Approve a match request.
        
        Args:
            request_id (int): Request's ID
            
        Returns:
            tuple: (success boolean, message)
        """
        request = Request.query.get(request_id)
        
        if not request:
            logger.warning(f"Request approval attempt for non-existent request ID: {request_id}")
            return False, "Request does not exist"
        
        if request.status != 'pending':
            logger.warning(f"Request approval attempt for non-pending request ID: {request_id}")
            return False, "Request is not pending"
        
        try:
            request.status = 'approved'
            db.session.commit()
            
            logger.info(f"Request approved: ID {request_id}")
            return True, "Request approved successfully"
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error approving request: {str(e)}")
            return False, f"Error approving request: {str(e)}"
    
    @staticmethod
    def reject_request(request_id):
        """
        Reject a match request.
        
        Args:
            request_id (int): Request's ID
            
        Returns:
            tuple: (success boolean, message)
        """
        request = Request.query.get(request_id)
        
        if not request:
            logger.warning(f"Request rejection attempt for non-existent request ID: {request_id}")
            return False, "Request does not exist"
        
        if request.status != 'pending':
            logger.warning(f"Request rejection attempt for non-pending request ID: {request_id}")
            return False, "Request is not pending"
        
        try:
            request.status = 'rejected'
            db.session.commit()
            
            logger.info(f"Request rejected: ID {request_id}")
            return True, "Request rejected successfully"
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error rejecting request: {str(e)}")
            return False, f"Error rejecting request: {str(e)}"
    
    @staticmethod
    def export_data(table_name):
        """
        Export data from a table to CSV.
        
        Args:
            table_name (str): Name of the table to export
            
        Returns:
            tuple: (CSV data as string, error message)
        """
        try:
            if table_name == 'user':
                # Export users (excluding passwords)
                users = User.query.all()
                data = [{
                    'id': user.id,
                    'fullname': user.fullname,
                    'phone_number': user.phone_number,
                    'created_at': user.created_at,
                    'is_admin': user.is_admin
                } for user in users]
                
            elif table_name == 'profile':
                # Export profiles
                profiles = Profile.query.all()
                data = [{
                    'id': profile.id,
                    'user_id': profile.user_id,
                    'created_at': profile.created_at,
                    'nationality': profile.nationality,
                    'age': profile.age,
                    'gender': profile.gender.value if profile.gender else None,
                    'city': profile.city,
                    'marital_status': profile.marital_status.status_name if profile.marital_status else None
                } for profile in profiles]
                
            elif table_name == 'request':
                # Export requests
                requests = Request.query.all()
                data = [{
                    'id': request.id,
                    'requester_id': request.requester_id,
                    'target_id': request.target_id,
                    'request_date': request.request_date,
                    'status': request.status
                } for request in requests]
                
            elif table_name == 'marital_status':
                # Export marital statuses
                statuses = MaritalStatus.query.all()
                data = [{
                    'id': status.id,
                    'status_name': status.status_name
                } for status in statuses]
                
            else:
                logger.warning(f"Export attempt for unknown table: {table_name}")
                return None, f"Unknown table: {table_name}"
            
            # Convert to DataFrame and then to CSV
            df = pd.DataFrame(data)
            csv_data = df.to_csv(index=False)
            
            logger.info(f"Data exported from table: {table_name}")
            return csv_data, None
            
        except Exception as e:
            logger.error(f"Error exporting data: {str(e)}")
            return None, f"Error exporting data: {str(e)}"

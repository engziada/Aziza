from app.models import db, Request, Profile, User
from app.utils import send_whatsapp_notification
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class RequestService:
    """Service class for match request-related operations."""
    
    @staticmethod
    def create_request(requester_id, target_id):
        """
        Create a new match request.
        
        Args:
            requester_id (int): Requester's profile ID
            target_id (int): Target's profile ID
            
        Returns:
            tuple: (Request object, error message)
        """
        # Check if profiles exist
        requester = Profile.query.get(requester_id)
        target = Profile.query.get(target_id)
        
        if not requester:
            logger.warning(f"Request creation attempt from non-existent profile ID: {requester_id}")
            return None, "Requester profile does not exist"
        
        if not target:
            logger.warning(f"Request creation attempt to non-existent profile ID: {target_id}")
            return None, "Target profile does not exist"
        
        # Check if request already exists
        existing_request = Request.query.filter_by(
            requester_id=requester_id,
            target_id=target_id
        ).first()
        
        if existing_request:
            logger.info(f"Duplicate request attempt from {requester_id} to {target_id}")
            return None, "Request already exists"
        
        # Create new request
        try:
            request = Request(
                requester_id=requester_id,
                target_id=target_id,
                request_date=datetime.utcnow(),
                status='pending'
            )
            
            db.session.add(request)
            db.session.commit()
            
            # Send notification to target user
            target_user = User.query.get(target.user_id)
            if target_user:
                message = f"You have received a new match request from {requester.user.fullname}"
                send_whatsapp_notification(target_user.phone_number, message)
            
            logger.info(f"New request created from {requester_id} to {target_id}")
            return request, None
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating request: {str(e)}")
            return None, f"Error creating request: {str(e)}"
    
    @staticmethod
    def update_request_status(request_id, status):
        """
        Update a request's status.
        
        Args:
            request_id (int): Request ID
            status (str): New status ('accepted', 'rejected', 'pending')
            
        Returns:
            tuple: (Request object, error message)
        """
        request = Request.query.get(request_id)
        
        if not request:
            logger.warning(f"Request status update attempt for non-existent request ID: {request_id}")
            return None, "Request does not exist"
        
        try:
            request.status = status
            db.session.commit()
            
            # Send notification to requester
            requester_user = User.query.get(request.requester.user_id)
            if requester_user:
                message = f"Your match request has been {status}"
                send_whatsapp_notification(requester_user.phone_number, message)
            
            logger.info(f"Request {request_id} status updated to {status}")
            return request, None
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating request status: {str(e)}")
            return None, f"Error updating request status: {str(e)}"
    
    @staticmethod
    def get_sent_requests(profile_id):
        """
        Get all requests sent by a profile.
        
        Args:
            profile_id (int): Profile ID
            
        Returns:
            list: List of sent requests
        """
        return Request.query.filter_by(requester_id=profile_id).all()
    
    @staticmethod
    def get_received_requests(profile_id):
        """
        Get all requests received by a profile.
        
        Args:
            profile_id (int): Profile ID
            
        Returns:
            list: List of received requests
        """
        return Request.query.filter_by(target_id=profile_id).all()
    
    @staticmethod
    def delete_request(request_id):
        """
        Delete a request.
        
        Args:
            request_id (int): Request ID
            
        Returns:
            tuple: (success boolean, message)
        """
        request = Request.query.get(request_id)
        
        if not request:
            logger.warning(f"Request deletion attempt for non-existent request ID: {request_id}")
            return False, "Request does not exist"
        
        try:
            db.session.delete(request)
            db.session.commit()
            
            logger.info(f"Request {request_id} deleted")
            return True, "Request deleted successfully"
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting request: {str(e)}")
            return False, f"Error deleting request: {str(e)}"

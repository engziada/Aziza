from app.models import db, Profile, User, Gender, MaritalStatus
import logging

logger = logging.getLogger(__name__)

class ProfileService:
    """Service class for profile-related operations."""
    
    @staticmethod
    def get_profile(user_id):
        """
        Get a user's profile.
        
        Args:
            user_id (int): User's ID
            
        Returns:
            Profile: User's profile or None if not found
        """
        return Profile.query.filter_by(user_id=user_id).first()
    
    @staticmethod
    def create_profile(user_id, profile_data):
        """
        Create a new profile for a user.
        
        Args:
            user_id (int): User's ID
            profile_data (dict): Profile data
            
        Returns:
            tuple: (Profile object, error message)
        """
        # Check if user exists
        user = User.query.get(user_id)
        if not user:
            logger.warning(f"Profile creation attempt for non-existent user ID: {user_id}")
            return None, "User does not exist"
        
        # Check if profile already exists
        existing_profile = Profile.query.filter_by(user_id=user_id).first()
        if existing_profile:
            logger.info(f"Profile creation attempt for user with existing profile: {user_id}")
            return None, "User already has a profile"
        
        # Create new profile
        try:
            profile = Profile(user_id=user_id)
            
            # Update profile with provided data
            for key, value in profile_data.items():
                if hasattr(profile, key):
                    setattr(profile, key, value)
            
            db.session.add(profile)
            db.session.commit()
            
            logger.info(f"New profile created for user ID: {user_id}")
            return profile, None
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating profile: {str(e)}")
            return None, f"Error creating profile: {str(e)}"
    
    @staticmethod
    def update_profile(profile_id, profile_data):
        """
        Update a user's profile.
        
        Args:
            profile_id (int): Profile ID
            profile_data (dict): Updated profile data
            
        Returns:
            tuple: (Profile object, error message)
        """
        profile = Profile.query.get(profile_id)
        
        if not profile:
            logger.warning(f"Profile update attempt for non-existent profile ID: {profile_id}")
            return None, "Profile does not exist"
        
        try:
            # Update profile with provided data
            for key, value in profile_data.items():
                if hasattr(profile, key):
                    setattr(profile, key, value)
            
            db.session.commit()
            
            logger.info(f"Profile updated for ID: {profile_id}")
            return profile, None
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating profile: {str(e)}")
            return None, f"Error updating profile: {str(e)}"
    
    @staticmethod
    def search_profiles(search_criteria):
        """
        Search for profiles based on criteria.
        
        Args:
            search_criteria (dict): Search criteria
            
        Returns:
            list: List of matching profiles
        """
        query = Profile.query
        
        # Apply filters based on search criteria
        if 'gender' in search_criteria and search_criteria['gender']:
            query = query.filter(Profile.gender == search_criteria['gender'])
        
        if 'min_age' in search_criteria and search_criteria['min_age']:
            query = query.filter(Profile.age >= search_criteria['min_age'])
        
        if 'max_age' in search_criteria and search_criteria['max_age']:
            query = query.filter(Profile.age <= search_criteria['max_age'])
        
        if 'nationality' in search_criteria and search_criteria['nationality']:
            query = query.filter(Profile.nationality == search_criteria['nationality'])
        
        if 'city' in search_criteria and search_criteria['city']:
            query = query.filter(Profile.city == search_criteria['city'])
        
        if 'marital_status_id' in search_criteria and search_criteria['marital_status_id']:
            query = query.filter(Profile.marital_status_id == search_criteria['marital_status_id'])
        
        # Execute query and return results
        profiles = query.all()
        logger.info(f"Profile search returned {len(profiles)} results")
        
        return profiles
    
    @staticmethod
    def delete_profile(profile_id):
        """
        Delete a user's profile.
        
        Args:
            profile_id (int): Profile ID
            
        Returns:
            tuple: (success boolean, message)
        """
        profile = Profile.query.get(profile_id)
        
        if not profile:
            logger.warning(f"Profile deletion attempt for non-existent profile ID: {profile_id}")
            return False, "Profile does not exist"
        
        try:
            db.session.delete(profile)
            db.session.commit()
            
            logger.info(f"Profile deleted for ID: {profile_id}")
            return True, "Profile deleted successfully"
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting profile: {str(e)}")
            return False, f"Error deleting profile: {str(e)}"

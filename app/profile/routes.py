from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services import ProfileService, RequestService
from app.models import Profile, Gender, MaritalStatus, SmokingStatus
from app.profile.forms import ProfileForm, SearchForm, RequestMatchForm
import logging

# Create blueprint
profile_bp = Blueprint('profile', __name__)
logger = logging.getLogger(__name__)

@profile_bp.route('/', methods=['GET', 'POST'])
def home():
    """Handle home page and search functionality."""
    # Check if user is logged in
    if 'user_id' not in session:
        flash('You must be logged in to access this page', 'danger')
        return redirect(url_for('auth.login'))
    
    # Get user's profile
    profile = ProfileService.get_profile(session['user_id'])
    
    # If user has no profile, redirect to profile creation
    if not profile:
        flash('Please create your profile first', 'info')
        return redirect(url_for('profile.edit_profile'))
    
    # Create search form
    form = SearchForm()
    
    # Initialize data dictionary with default values
    data = {
        'gender': 'MALE',
        'nationality': '',
        'min_age': 18,
        'max_age': 60,
        'min_height': 150,
        'max_height': 190,
        'min_weight': 50,
        'max_weight': 100,
        'color': '',
        'smoking': ''
    }
    
    # Handle search form submission
    profiles = None
    if request.method == 'POST':
        # Get form data
        data['gender'] = request.form.get('gender', 'MALE')
        data['nationality'] = request.form.get('nationality', '')
        data['min_age'] = int(request.form.get('min_age', 18))
        data['max_age'] = int(request.form.get('max_age', 60))
        data['min_height'] = int(request.form.get('min_height', 150))
        data['max_height'] = int(request.form.get('max_height', 190))
        data['min_weight'] = int(request.form.get('min_weight', 50))
        data['max_weight'] = int(request.form.get('max_weight', 100))
        data['color'] = request.form.get('color', '')
        data['smoking'] = request.form.get('smoking', '')
        
        # Build search criteria
        gender_enum = None
        if data['gender'] == 'MALE':
            gender_enum = Gender.MALE
        elif data['gender'] == 'FEMALE':
            gender_enum = Gender.FEMALE
        
        smoking_status = None
        if data['smoking'] == '1':
            smoking_status = SmokingStatus.SMOKER
        elif data['smoking'] == '0':
            smoking_status = SmokingStatus.NON_SMOKER
        
        # Build search criteria
        search_criteria = {
            'gender': gender_enum,
            'min_age': data['min_age'],
            'max_age': data['max_age'],
            'nationality': data['nationality'] if data['nationality'] else None,
            'skin_color': data['color'] if data['color'] else None,
            'min_height': data['min_height'],
            'max_height': data['max_height'],
            'min_weight': data['min_weight'],
            'max_weight': data['max_weight'],
            'smoking_status': smoking_status
        }
        
        # Search for profiles
        profiles = ProfileService.search_profiles(search_criteria)
        logger.info(f"Search returned {len(profiles)} results")
    
    # Return template with form, data, and search results
    return render_template('home.html', form=form, data=data, profiles=profiles)

@profile_bp.route('/profile', methods=['GET', 'POST'])
def edit_profile():
    """Handle profile creation and editing."""
    # Check if user is logged in
    if 'user_id' not in session:
        flash('You must be logged in to access this page', 'danger')
        return redirect(url_for('auth.login'))
    
    # Get user's profile if it exists
    profile = ProfileService.get_profile(session['user_id'])
    
    # Create form
    form = ProfileForm()
    
    # If it's a GET request and profile exists, populate form with profile data
    if request.method == 'GET' and profile:
        form.gender.data = profile.gender.name if profile.gender else None
        form.age.data = profile.age
        form.nationality.data = profile.nationality
        form.height.data = profile.height
        form.weight.data = profile.weight
        form.skin_color.data = profile.skin_color
        form.employment_status.data = profile.job_status
        form.tribe.data = profile.tribe
        form.smoking.data = profile.smoking_status == SmokingStatus.SMOKER if profile.smoking_status else False
        form.marital_status.data = profile.marital_status_id
        form.education.data = profile.qualifications
        form.city.data = profile.city
        form.area.data = profile.area
        form.marriage_type.data = profile.marriage_type
        form.another_nationality.data = profile.another_nationality
        form.description.data = profile.about
        form.partner_requirements.data = profile.requirements
    
    if form.validate_on_submit():
        # Convert form data to gender enum
        gender_value = form.gender.data.upper()
        gender_enum = None
        if gender_value == 'MALE':
            gender_enum = Gender.MALE
        elif gender_value == 'FEMALE':
            gender_enum = Gender.FEMALE
        
        # Convert smoking checkbox to enum
        smoking_status = SmokingStatus.SMOKER if form.smoking.data else SmokingStatus.NON_SMOKER
        
        # Collect profile data from form
        profile_data = {
            'user_id': session['user_id'],
            'gender': gender_enum,
            'age': form.age.data,
            'nationality': form.nationality.data,
            'height': form.height.data,
            'weight': form.weight.data,
            'skin_color': form.skin_color.data,
            'job_status': form.employment_status.data,
            'tribe': form.tribe.data,
            'smoking_status': smoking_status,
            'marital_status_id': form.marital_status.data,
            'qualifications': form.education.data,
            'city': form.city.data,
            'area': form.area.data,
            'marriage_type': form.marriage_type.data,
            'another_nationality': form.another_nationality.data,
            'about': form.description.data,
            'requirements': form.partner_requirements.data
        }
        
        # Create or update profile
        if profile:
            ProfileService.update_profile(profile.id, profile_data)
            flash('Profile updated successfully', 'success')
        else:
            ProfileService.create_profile(session['user_id'], profile_data)
            flash('Profile created successfully', 'success')
        
        return redirect(url_for('profile.home'))
    
    return render_template('profile.html', form=form)

@profile_bp.route('/search', methods=['GET', 'POST'])
def search():
    """Handle profile search."""
    # Check if user is logged in
    if 'user_id' not in session:
        flash('You must be logged in to access this page', 'danger')
        return redirect(url_for('auth.login'))
    
    # Create search form
    form = SearchForm()
    
    if form.validate_on_submit():
        # Get gender enum from form data
        gender_value = form.gender.data.upper() if form.gender.data else None
        gender_enum = None
        if gender_value == 'MALE':
            gender_enum = Gender.MALE
        elif gender_value == 'FEMALE':
            gender_enum = Gender.FEMALE
        
        # Build search criteria from form data
        search_criteria = {
            'gender': gender_enum,
            'min_age': form.ageMin.data,
            'max_age': form.ageMax.data,
            'nationality': form.nationality.data if form.nationality.data else None,
            'skin_color': form.color.data if form.color.data else None,
            'min_height': form.lengthMin.data,
            'max_height': form.lengthMax.data,
            'min_weight': form.weightMin.data,
            'max_weight': form.weightMax.data
        }
        
        # Search for profiles
        profiles = ProfileService.search_profiles(search_criteria)
        
        return render_template('search_results.html', profiles=profiles)
    
    return render_template('search.html', form=form)

@profile_bp.route('/request_match', methods=['GET', 'POST'])
def request_match():
    """Handle match request."""
    # Check if user is logged in
    if 'user_id' not in session:
        flash('You must be logged in to access this page', 'danger')
        return redirect(url_for('auth.login'))
    
    # Get user's profile
    profile = ProfileService.get_profile(session['user_id'])
    
    # If user has no profile, redirect to profile creation
    if not profile:
        flash('Please create your profile first', 'info')
        return redirect(url_for('profile.edit_profile'))
    
    # For POST requests from the home page
    if request.method == 'POST':
        try:
            # Get the target profile ID from the form
            target_id = request.form.get('profile_id')
            
            if not target_id:
                flash('معرف الملف الشخصي غير صالح', 'danger')
                return redirect(url_for('profile.home'))
            
            # Create match request
            result = RequestService.create_request(profile.id, target_id)
            
            if result:
                flash('تم إرسال طلب التعارف بنجاح', 'success')
            else:
                flash('فشل في إرسال طلب التعارف', 'danger')
                
        except Exception as e:
            logger.error(f"Error creating match request: {str(e)}")
            flash('حدث خطأ أثناء إرسال طلب التعارف', 'danger')
    
    return redirect(url_for('profile.home'))

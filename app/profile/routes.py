from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services import ProfileService
from app.models import Profile, Gender, MaritalStatus
import logging

# Create blueprint
profile_bp = Blueprint('profile', __name__)
logger = logging.getLogger(__name__)

@profile_bp.route('/')
def home():
    """Display the home page."""
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
    
    return render_template('home.html', profile=profile)

@profile_bp.route('/profile', methods=['GET', 'POST'])
def edit_profile():
    """Handle profile creation and editing."""
    # Check if user is logged in
    if 'user_id' not in session:
        flash('You must be logged in to access this page', 'danger')
        return redirect(url_for('auth.login'))
    
    # Get user's profile
    profile = ProfileService.get_profile(session['user_id'])
    
    # Get all marital statuses for the form
    marital_statuses = MaritalStatus.query.all()
    
    if request.method == 'POST':
        # Collect form data
        profile_data = {
            'nationality': request.form.get('nationality'),
            'age': int(request.form.get('age')) if request.form.get('age') else None,
            'height': int(request.form.get('height')) if request.form.get('height') else None,
            'weight': int(request.form.get('weight')) if request.form.get('weight') else None,
            'skin_color': request.form.get('color'),
            'job_status': request.form.get('jobstatus'),
            'tribe': request.form.get('qabila'),
            'smoking_status': int(request.form.get('smokingstatus')) if request.form.get('smokingstatus') else None,
            'marital_status_id': int(request.form.get('martialstatus')) if request.form.get('martialstatus') else None,
            'area': request.form.get('area'),
            'city': request.form.get('city'),
            'origin': request.form.get('origin'),
            'qualifications': request.form.get('qualifications'),
            'marriage_type': request.form.get('marriagetype'),
            'another_nationality': bool(int(request.form.get('anothernationality'))) if request.form.get('anothernationality') else False,
            'about': request.form.get('about'),
            'requirements': request.form.get('requirments'),
            'gender': request.form.get('gender')
        }
        
        if profile:
            # Update existing profile
            updated_profile, error = ProfileService.update_profile(profile.id, profile_data)
            
            if error:
                flash(error, 'danger')
                return render_template('profile.html', profile=profile, marital_statuses=marital_statuses)
            
            flash('Profile updated successfully', 'success')
        else:
            # Create new profile
            new_profile, error = ProfileService.create_profile(session['user_id'], profile_data)
            
            if error:
                flash(error, 'danger')
                return render_template('profile.html', profile=None, marital_statuses=marital_statuses)
            
            flash('Profile created successfully', 'success')
        
        return redirect(url_for('profile.home'))
    
    return render_template('profile.html', profile=profile, marital_statuses=marital_statuses)

@profile_bp.route('/search', methods=['GET', 'POST'])
def search():
    """Handle profile search."""
    # Check if user is logged in
    if 'user_id' not in session:
        flash('You must be logged in to access this page', 'danger')
        return redirect(url_for('auth.login'))
    
    # Get all marital statuses for the form
    marital_statuses = MaritalStatus.query.all()
    
    if request.method == 'POST':
        # Collect search criteria
        search_criteria = {
            'gender': request.form.get('gender'),
            'min_age': int(request.form.get('min_age')) if request.form.get('min_age') else None,
            'max_age': int(request.form.get('max_age')) if request.form.get('max_age') else None,
            'nationality': request.form.get('nationality'),
            'city': request.form.get('city'),
            'marital_status_id': int(request.form.get('martialstatus')) if request.form.get('martialstatus') else None
        }
        
        # Search for profiles
        profiles = ProfileService.search_profiles(search_criteria)
        
        return render_template('search_results.html', profiles=profiles)
    
    return render_template('search.html', marital_statuses=marital_statuses)

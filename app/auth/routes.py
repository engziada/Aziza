from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services import AuthService
from app.models import User
import logging

# Create blueprint
auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        phone_number = request.form.get('username')
        password = request.form.get('password')
        
        if not phone_number or not password:
            flash('Please provide both phone number and password', 'danger')
            return render_template('login.html')
        
        user, error = AuthService.login(phone_number, password)
        
        if error:
            flash(error, 'danger')
            return render_template('login.html')
        
        # Set session variables
        session['user_id'] = user.id
        session['fullname'] = user.fullname
        session['is_admin'] = user.is_admin
        
        flash(f'Welcome back, {user.fullname}!', 'success')
        return redirect(url_for('profile.home'))
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """Handle user logout."""
    # Clear session
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        phone_number = request.form.get('phoneno')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate input
        if not fullname or not phone_number or not password:
            flash('Please fill in all fields', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')
        
        user, error = AuthService.register(fullname, phone_number, password)
        
        if error:
            flash(error, 'danger')
            return render_template('register.html')
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/forget-password', methods=['GET', 'POST'])
def forget_password():
    """Handle password reset requests."""
    if request.method == 'POST':
        phone_number = request.form.get('phoneno')
        
        if not phone_number:
            flash('Please provide your phone number', 'danger')
            return render_template('forget_password.html')
        
        success, message = AuthService.reset_password(phone_number)
        
        if not success:
            flash(message, 'danger')
            return render_template('forget_password.html')
        
        flash(message, 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('forget_password.html')

@auth_bp.route('/change-password', methods=['GET', 'POST'])
def change_password():
    """Handle password change requests."""
    # Check if user is logged in
    if 'user_id' not in session:
        flash('You must be logged in to change your password', 'danger')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate input
        if not current_password or not new_password or not confirm_password:
            flash('Please fill in all fields', 'danger')
            return render_template('change_password.html')
        
        if new_password != confirm_password:
            flash('New passwords do not match', 'danger')
            return render_template('change_password.html')
        
        success, message = AuthService.change_password(
            session['user_id'], 
            current_password, 
            new_password
        )
        
        if not success:
            flash(message, 'danger')
            return render_template('change_password.html')
        
        flash(message, 'success')
        return redirect(url_for('profile.home'))
    
    return render_template('change_password.html')

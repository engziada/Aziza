from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services import AuthService
from app.models import User, db
from app.auth.forms import LoginForm, RegistrationForm, ForgetPasswordForm, ChangePasswordForm
import logging

# Create blueprint
auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    form = LoginForm()
    
    if form.validate_on_submit():
        phone_number = form.username.data
        password = form.password.data
        
        user, error = AuthService.login(phone_number, password)
        
        if error:
            flash(error, 'danger')
            return render_template('login.html', form=form)
        
        # Set session variables
        session['user_id'] = user.id
        session['fullname'] = user.fullname
        session['is_admin'] = user.is_admin
        
        flash(f'Welcome back, {user.fullname}!', 'success')
        return redirect(url_for('profile.home'))
    
    return render_template('login.html', form=form)

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
    form = RegistrationForm()
    
    if form.validate_on_submit():
        fullname = form.fullname.data
        phone_number = form.phoneno.data
        password = form.password.data
        
        user, error = AuthService.register(fullname, phone_number, password)
        
        if error:
            flash(error, 'danger')
            return render_template('register.html', form=form)
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)

@auth_bp.route('/forget-password', methods=['GET', 'POST'])
def forget_password():
    """Handle password reset requests."""
    form = ForgetPasswordForm()
    
    if form.validate_on_submit():
        phone_number = form.phoneno.data
        
        success, message = AuthService.reset_password(phone_number)
        
        if not success:
            flash(message, 'danger')
            return render_template('forget_password.html', form=form)
        
        flash(message, 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('forget_password.html', form=form)

@auth_bp.route('/change-password', methods=['GET', 'POST'])
def change_password():
    """Handle password change requests."""
    # Check if user is logged in
    if 'user_id' not in session:
        flash('You must be logged in to change your password', 'danger')
        return redirect(url_for('auth.login'))
    
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data
        confirm_password = form.confirm_password.data
        
        # Validate new password
        if new_password != confirm_password:
            flash('New passwords do not match', 'danger')
            return render_template('change_password.html', form=form)
        
        # Get user
        user = User.query.get(session['user_id'])
        
        # Check if current password is correct
        if not user.check_password(current_password):
            flash('Current password is incorrect', 'danger')
            return render_template('change_password.html', form=form)
        
        # Update password
        user.set_password(new_password)
        db.session.commit()
        
        flash('Password changed successfully', 'success')
        return redirect(url_for('profile.home'))
    
    return render_template('change_password.html', form=form)

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services import AdminService
from app.models import User, Request, Profile
from app.admin.forms import ApproveRequestForm, RejectRequestForm, DeleteUserForm
import logging

# Create blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
logger = logging.getLogger(__name__)

@admin_bp.route('/requests')
def requests():
    """Display all match requests."""
    # Check if user is logged in and is admin
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('You must be an admin to access this page', 'danger')
        return redirect(url_for('auth.login'))
    
    # Get all requests
    all_requests = Request.query.all()
    
    # Create forms for each request
    approve_forms = {}
    reject_forms = {}
    for req in all_requests:
        approve_form = ApproveRequestForm()
        approve_form.request_id.data = req.id
        approve_forms[req.id] = approve_form
        
        reject_form = RejectRequestForm()
        reject_form.request_id.data = req.id
        reject_forms[req.id] = reject_form
    
    return render_template('admin/requests.html', requests=all_requests, 
                          approve_forms=approve_forms, reject_forms=reject_forms)

@admin_bp.route('/users')
def users():
    """Display all users."""
    # Check if user is logged in and is admin
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('You must be an admin to access this page', 'danger')
        return redirect(url_for('auth.login'))
    
    # Get all users
    all_users = User.query.all()
    
    # Create delete forms for each user
    delete_forms = {}
    for user in all_users:
        delete_form = DeleteUserForm()
        delete_form.user_id.data = user.id
        delete_forms[user.id] = delete_form
    
    return render_template('admin/users.html', users=all_users, delete_forms=delete_forms)

@admin_bp.route('/approve-request/<int:request_id>', methods=['POST'])
def approve_request(request_id):
    """Approve a match request."""
    # Check if user is logged in and is admin
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('You must be an admin to access this page', 'danger')
        return redirect(url_for('auth.login'))
    
    form = ApproveRequestForm()
    
    if form.validate_on_submit():
        # Approve request
        success, message = AdminService.approve_request(request_id)
        
        if success:
            flash(message, 'success')
        else:
            flash(message, 'danger')
    
    return redirect(url_for('admin.requests'))

@admin_bp.route('/reject-request/<int:request_id>', methods=['POST'])
def reject_request(request_id):
    """Reject a match request."""
    # Check if user is logged in and is admin
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('You must be an admin to access this page', 'danger')
        return redirect(url_for('auth.login'))
    
    form = RejectRequestForm()
    
    if form.validate_on_submit():
        # Reject request
        success, message = AdminService.reject_request(request_id)
        
        if success:
            flash(message, 'success')
        else:
            flash(message, 'danger')
    
    return redirect(url_for('admin.requests'))

@admin_bp.route('/delete-user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    """Delete a user."""
    # Check if user is logged in and is admin
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('You must be an admin to access this page', 'danger')
        return redirect(url_for('auth.login'))
    
    form = DeleteUserForm()
    
    if form.validate_on_submit():
        # Delete user
        success, message = AdminService.delete_user(user_id)
        
        if success:
            flash(message, 'success')
        else:
            flash(message, 'danger')
    
    return redirect(url_for('admin.users'))

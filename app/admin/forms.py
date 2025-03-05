from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField
from wtforms.validators import DataRequired

class ApproveRequestForm(FlaskForm):
    """Form for approving a match request."""
    request_id = HiddenField('معرف الطلب', validators=[DataRequired()])
    submit = SubmitField('موافقة')

class RejectRequestForm(FlaskForm):
    """Form for rejecting a match request."""
    request_id = HiddenField('معرف الطلب', validators=[DataRequired()])
    submit = SubmitField('رفض')

class DeleteUserForm(FlaskForm):
    """Form for deleting a user."""
    user_id = HiddenField('معرف المستخدم', validators=[DataRequired()])
    submit = SubmitField('حذف')

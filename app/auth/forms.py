from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    """Form for user login."""
    username = StringField('رقم الهاتف', validators=[DataRequired(message='رقم الهاتف مطلوب')])
    password = PasswordField('كلمة المرور', validators=[DataRequired(message='كلمة المرور مطلوبة')])
    submit = SubmitField('تسجيل الدخول')

class RegistrationForm(FlaskForm):
    """Form for user registration."""
    fullname = StringField('الاسم الكامل', validators=[
        DataRequired(message='الاسم الكامل مطلوب'),
        Length(min=3, max=128, message='يجب أن يكون الاسم بين 3 و 128 حرفًا')
    ])
    phoneno = StringField('رقم الهاتف', validators=[
        DataRequired(message='رقم الهاتف مطلوب'),
        Length(min=10, max=15, message='يجب أن يكون رقم الهاتف بين 10 و 15 رقمًا')
    ])
    password = PasswordField('كلمة المرور', validators=[
        DataRequired(message='كلمة المرور مطلوبة'),
        Length(min=6, message='يجب أن تكون كلمة المرور 6 أحرف على الأقل')
    ])
    confirm_password = PasswordField('تأكيد كلمة المرور', validators=[
        DataRequired(message='تأكيد كلمة المرور مطلوب'),
        EqualTo('password', message='كلمات المرور غير متطابقة')
    ])
    submit = SubmitField('تسجيل')

    def validate_phoneno(self, phoneno):
        """Validate that the phone number is not already registered."""
        user = User.query.filter_by(phone_number=phoneno.data).first()
        if user:
            raise ValidationError('رقم الهاتف مسجل بالفعل. الرجاء استخدام رقم آخر أو تسجيل الدخول.')

class ForgetPasswordForm(FlaskForm):
    """Form for password reset requests."""
    phoneno = StringField('رقم الهاتف', validators=[
        DataRequired(message='رقم الهاتف مطلوب'),
        Length(min=10, max=15, message='يجب أن يكون رقم الهاتف بين 10 و 15 رقمًا')
    ])
    submit = SubmitField('إرسال كلمة مرور جديدة')

class ChangePasswordForm(FlaskForm):
    """Form for changing password."""
    current_password = PasswordField('كلمة المرور الحالية', validators=[
        DataRequired(message='كلمة المرور الحالية مطلوبة')
    ])
    new_password = PasswordField('كلمة المرور الجديدة', validators=[
        DataRequired(message='كلمة المرور الجديدة مطلوبة'),
        Length(min=6, message='يجب أن تكون كلمة المرور 6 أحرف على الأقل')
    ])
    confirm_password = PasswordField('تأكيد كلمة المرور الجديدة', validators=[
        DataRequired(message='تأكيد كلمة المرور مطلوب'),
        EqualTo('new_password', message='كلمات المرور غير متطابقة')
    ])
    submit = SubmitField('تغيير كلمة المرور')

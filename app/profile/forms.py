from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, NumberRange, Optional, Length
from app.models import Gender, SmokingStatus, MaritalStatus

class ProfileForm(FlaskForm):
    """Form for profile creation and editing."""
    gender = SelectField('الجنس', choices=[
        ('MALE', 'ذكر'),
        ('FEMALE', 'أنثى')
    ], validators=[DataRequired(message='الجنس مطلوب')])
    
    age = IntegerField('العمر', validators=[
        DataRequired(message='العمر مطلوب'),
        NumberRange(min=18, max=100, message='العمر يجب أن يكون بين 18 و 100')
    ])
    
    nationality = StringField('الجنسية', validators=[
        DataRequired(message='الجنسية مطلوبة'),
        Length(max=45, message='الجنسية يجب أن تكون أقل من 45 حرفًا')
    ])
    
    height = IntegerField('الطول (سم)', validators=[
        DataRequired(message='الطول مطلوب'),
        NumberRange(min=100, max=250, message='الطول يجب أن يكون بين 100 و 250 سم')
    ])
    
    weight = IntegerField('الوزن (كجم)', validators=[
        DataRequired(message='الوزن مطلوب'),
        NumberRange(min=30, max=200, message='الوزن يجب أن يكون بين 30 و 200 كجم')
    ])
    
    skin_color = StringField('لون البشرة', validators=[
        Optional(),
        Length(max=45, message='لون البشرة يجب أن يكون أقل من 45 حرفًا')
    ])
    
    employment_status = StringField('الحالة الوظيفية', validators=[
        Optional(),
        Length(max=255, message='الحالة الوظيفية يجب أن تكون أقل من 255 حرفًا')
    ])
    
    tribe = StringField('القبيلة', validators=[
        Optional(),
        Length(max=45, message='القبيلة يجب أن تكون أقل من 45 حرفًا')
    ])
    
    smoking = BooleanField('مدخن')
    
    marital_status = SelectField('الحالة الاجتماعية', coerce=int, validators=[
        DataRequired(message='الحالة الاجتماعية مطلوبة')
    ])
    
    education = StringField('المؤهل الدراسي', validators=[
        Optional(),
        Length(max=45, message='المؤهل الدراسي يجب أن يكون أقل من 45 حرفًا')
    ])
    
    city = StringField('المدينة', validators=[
        DataRequired(message='المدينة مطلوبة'),
        Length(max=45, message='المدينة يجب أن تكون أقل من 45 حرفًا')
    ])
    
    area = StringField('المنطقة', validators=[
        Optional(),
        Length(max=45, message='المنطقة يجب أن تكون أقل من 45 حرفًا')
    ])
    
    marriage_type = StringField('نوع الزواج', validators=[
        Optional(),
        Length(max=45, message='نوع الزواج يجب أن يكون أقل من 45 حرفًا')
    ])
    
    another_nationality = BooleanField('جنسية أخرى')
    
    description = TextAreaField('نبذة عن الشخص', validators=[
        Optional(),
        Length(max=1000, message='النبذة يجب أن تكون أقل من 1000 حرف')
    ])
    
    partner_requirements = TextAreaField('متطلبات الشريك', validators=[
        Optional(),
        Length(max=1000, message='المتطلبات يجب أن تكون أقل من 1000 حرف')
    ])
    
    submit = SubmitField('حفظ')
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # Populate marital status choices
        marital_statuses = MaritalStatus.query.all()
        self.marital_status.choices = [(status.id, status.status_name) for status in marital_statuses]

class SearchForm(FlaskForm):
    """Form for profile search."""
    gender = SelectField('الجنس', choices=[
        ('', 'الكل'),
        ('MALE', 'ذكر'),
        ('FEMALE', 'أنثى')
    ], validators=[Optional()])
    
    ageMin = IntegerField('العمر من', validators=[
        Optional(),
        NumberRange(min=18, max=100, message='العمر يجب أن يكون بين 18 و 100')
    ], default=20)
    
    ageMax = IntegerField('العمر إلى', validators=[
        Optional(),
        NumberRange(min=18, max=100, message='العمر يجب أن يكون بين 18 و 100')
    ], default=80)
    
    nationality = StringField('الجنسية', validators=[
        Optional(),
        Length(max=45, message='الجنسية يجب أن تكون أقل من 45 حرفًا')
    ])
    
    color = StringField('لون البشرة', validators=[
        Optional(),
        Length(max=45, message='لون البشرة يجب أن يكون أقل من 45 حرفًا')
    ])
    
    lengthMin = IntegerField('الطول من (سم)', validators=[
        Optional(),
        NumberRange(min=100, max=250, message='الطول يجب أن يكون بين 100 و 250 سم')
    ], default=150)
    
    lengthMax = IntegerField('الطول إلى (سم)', validators=[
        Optional(),
        NumberRange(min=100, max=250, message='الطول يجب أن يكون بين 100 و 250 سم')
    ], default=170)
    
    weightMin = IntegerField('الوزن من (كجم)', validators=[
        Optional(),
        NumberRange(min=30, max=200, message='الوزن يجب أن يكون بين 30 و 200 كجم')
    ], default=60)
    
    weightMax = IntegerField('الوزن إلى (كجم)', validators=[
        Optional(),
        NumberRange(min=30, max=200, message='الوزن يجب أن يكون بين 30 و 200 كجم')
    ], default=100)
    
    smokingstatus = SelectField('التدخين', choices=[
        ('', 'الكل'),
        ('0', 'غير مدخن'),
        ('1', 'مدخن')
    ], validators=[Optional()])
    
    submit = SubmitField('بحث')

class RequestMatchForm(FlaskForm):
    """Form for requesting a match."""
    idman = IntegerField('معرف الملف الشخصي', validators=[DataRequired()])
    submit = SubmitField('طلب')

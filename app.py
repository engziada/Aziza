from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, Profile, MartialStatus, Request
from werkzeug.security import generate_password_hash, check_password_hash
import os
import pandas as pd
import io, string
from random import choices
from flask import make_response

# Create Flask application
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '12qwaszx#E')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dating.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database with app
db.init_app(app)

# Ensure the Logs directory exists
if not os.path.exists('Logs'):
    os.makedirs('Logs')

def checkPassword(username:str, password:str) -> int:
    """
    Check if the username and password match a user in the database.
    
    Args:
        username (str): The username (phone number)
        password (str): The password to check
        
    Returns:
        int: 0 if successful, -1 if password is incorrect, -2 if user doesn't exist
    """
    phoneno = username
    user = User.query.filter_by(phoneno=phoneno).first()
    
    # If account exists
    if user:
        # Check for password using the model's method
        if user.check_password(password):
            return 0
        else:
            return -1
    else:
        return -2

def updatePassword(username: str, password: str):
    """
    Update a user's password.
    
    Args:
        username (str): The username (phone number)
        password (str): The new password
    """
    phoneno = username
    newhashedpassword = generate_password_hash(password, method="pbkdf2:sha256")
    user = User.query.filter_by(phoneno=phoneno).first()
    if user:
        user.password = newhashedpassword
        db.session.commit()

def create_admin():
    """
    Create an admin account if it doesn't already exist.
    """
    admin_phoneno = '0000000'
    admin_password = generate_password_hash('admin', method="pbkdf2:sha256")
    admin_fullname = 'Administrator'
    try:
        # Check if admin is already registered
        existing_admin = User.query.filter_by(phoneno=admin_phoneno).first()
        if existing_admin:
            print('Administrator account already exists.')
        else:
            new_admin = User(fullname=admin_fullname, phoneno=admin_phoneno, password=admin_password)
            db.session.add(new_admin)
            db.session.commit()
            print(f'Administrator account created successfully with record id: {new_admin.iduser}')
    except Exception as e:
        print(e)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Handle user login.
    """
    # Output message if something goes wrong...
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST':
        # Create variables for easy access
        phoneno = request.form.get('phoneno')
        password = request.form.get('password')

        if 'login' in request.form and phoneno and password:
            # Check if account exists
            user = User.query.filter_by(phoneno=phoneno).first()

            # Check password
            if user:
                if user.check_password(password):
                    # Create session data
                    session['loggedin'] = True
                    session['userid'] = user.iduser
                    session['phoneno'] = user.phoneno
                    session['fullname'] = user.fullname

                    # Redirect to home page
                    return redirect(url_for('home'))
                else:
                    flash('كلمة المرور غير صحيحة')
            else:
                flash("المستخدم غير موجود")

        elif 'forgetpassword' in request.form:
            forgetpassword(request.form.get('targetphoneno'))
    return render_template('index.html')

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('phoneno', None)
    session.pop('fullname', None)
    # Redirect to login page
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Check if form submitted
    if request.method == 'POST' and 'fullname' in request.form and 'password' in request.form and 'phoneno' in request.form:
        # Create variables for easy access
        fullname = request.form['fullname']
        password = generate_password_hash(request.form['password'], method="pbkdf2:sha256")
        phoneno = request.form['phoneno']

        # Check if account exists
        existing_user = User.query.filter_by(phoneno=phoneno).first()
        
        # If account exists show error and validation checks
        if existing_user:
            flash('رقم الجوال موجود بالفعل')
        elif not fullname or not password or not phoneno:
            flash('من فضلك أكمل البيانات')
        else:
            # Account doesn't exist and the form data is valid, now insert new account
            new_user = User(fullname=fullname, phoneno=phoneno, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('تم التسجيل بنجاح')
            return redirect(url_for('login'))
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('من فضلك أكمل البيانات')
    # Show registration form with message (if any)
    return render_template('register.html')

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # Get user by ID from session
        user = User.query.get(session['userid'])
        
        # Check if user exists
        if user is None:
            # User not found in database, clear session and redirect to login
            session.clear()
            flash('جلسة غير صالحة، يرجى تسجيل الدخول مرة أخرى')
            return redirect(url_for('login'))
            
        # Check if the user has already a profile or not
        profile = Profile.query.filter_by(userid=user.iduser).first()
        if not profile:
            # User doesn't have a profile, redirect to profile page with a message
            flash('لابد من تسجيل بياناتك أولا حتى تستطيع إستخدام البحث')
            
            # Create a dictionary with user information for the template
            user_info = {
                'fullname': user.fullname,
                'phoneno': user.phoneno
            }
            
            # Initialize empty profile data with default values
            profile_data = {
                'nationality': '',
                'age': 18,
                'length': 160,
                'weight': 70,
                'color': '',
                'jobstatus': '',
                'qabila': '',
                'smokingstatus': 1,
                'martialstatus': 'أعزب',
                'area': '',
                'city': '',
                'origin': '',
                'qualifications': 'ثانوي',
                'marriagetype': '',
                'anothernationality': 1,
                'about': '',
                'requirments': '',
                'gender': 'ذكر'
            }
            
            # Show the profile page with account info
            return render_template('profile.html', account=user_info, data=profile_data)
            
        if request.method == 'POST':
            # In case of Search button pressed
            if "Search" in request.form:
                ageMin = request.form.get('ageMin')
                ageMax = request.form.get('ageMax')
                lengthMin = request.form.get('lengthMin')
                lengthMax = request.form.get('lengthMax')
                weightMin = request.form.get('weightMin')
                weightMax = request.form.get('weightMax')
                smokingstatus = request.form.get('smokingstatus')
                marriagetype = request.form.getlist('marriagetype')
                gender = request.form.get('gender')
                nationality = request.form.get('nationality')
                color = request.form.get('color')
                martialstatus = request.form.getlist('martialstatus')
                
                # Perform search using SQLAlchemy
                query = Profile.query.filter(
                    Profile.gender == gender,
                    Profile.smokingstatus == smokingstatus,
                    Profile.age.between(ageMin, ageMax),
                    Profile.length.between(lengthMin, lengthMax),
                    Profile.weight.between(weightMin, weightMax)
                )
                
                if nationality:
                    query = query.filter(Profile.nationality.like(f'%{nationality}%'))
                if color:
                    query = query.filter(Profile.color.like(f'%{color}%'))
                if marriagetype:
                    query = query.filter(Profile.marriagetype.in_(marriagetype))
                if martialstatus:
                    query = query.filter(Profile.martialstatus.in_(martialstatus))
                
                searchResults = query.all()
                return render_template('home.html', fullname=session.get('fullname'), searchResults=searchResults, data=request.form)

            # In case of Request button pressed
            elif "Request" in request.form:
                requesterid = request.form["requesterid"]
                targetid = request.form["targetid"]
                
                # Check if request already exists
                existing_request = Request.query.filter_by(idrequester=requesterid, idtarget=targetid).first()
                
                if existing_request:
                    flash('تم إرسال الطلب من قبل')
                    return render_template('home.html', fullname=session.get('fullname'), data=None)
                else:
                    # Create new request
                    new_request = Request(idrequester=requesterid, idtarget=targetid)
                    db.session.add(new_request)
                    db.session.commit()
                    flash('تم إرسال الطلب بنجاح')
                    return render_template('home.html', fullname=session.get('fullname'), data=None)
            
            # In case of Profile button pressed
            elif "Profile" in request.form:
                user = User.query.get(session['userid'])
                account = Profile.query.filter_by(userid=user.iduser).first()
                return render_template('profile.html', account=account, data=None)
            
            return render_template('home.html', fullname=session.get('fullname'), data=None)
        
        # GET request
        return render_template('home.html', fullname=session.get('fullname'), data=None)
    
    # User is not logged in, redirect to login page
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    # Check if user is logged in
    if 'loggedin' in session:
        # Get user by ID from session
        user = User.query.get(session['userid'])
        
        # Check if user exists
        if user is None:
            # User not found in database, clear session and redirect to login
            session.clear()
            flash('جلسة غير صالحة، يرجى تسجيل الدخول مرة أخرى')
            return redirect(url_for('login'))
            
        profile = Profile.query.filter_by(userid=user.iduser).first()
        
        if request.method == 'POST':
            # Handle profile update
            if 'Save' in request.form:
                # Get form data
                nationality = request.form.get('nationality')
                age = request.form.get('age')
                length = request.form.get('length')
                weight = request.form.get('weight')
                color = request.form.get('color')
                jobstatus = request.form.get('jobstatus')
                qabila = request.form.get('qabila')
                smokingstatus = request.form.get('smokingstatus')
                martialstatus = request.form.get('martialstatus')
                area = request.form.get('area')
                city = request.form.get('city')
                origin = request.form.get('origin')
                qualifications = request.form.get('qualifications')
                marriagetype = request.form.get('marriagetype')
                anothernationality = request.form.get('anothernationality')
                about = request.form.get('about')
                requirments = request.form.get('requirments')
                gender = request.form.get('gender')
                
                if profile:
                    # Update existing profile
                    profile.nationality = nationality
                    profile.age = age
                    profile.length = length
                    profile.weight = weight
                    profile.color = color
                    profile.jobstatus = jobstatus
                    profile.qabila = qabila
                    profile.smokingstatus = smokingstatus
                    profile.martialstatus = martialstatus
                    profile.area = area
                    profile.city = city
                    profile.origin = origin
                    profile.qualifications = qualifications
                    profile.marriagetype = marriagetype
                    profile.anothernationality = anothernationality
                    profile.about = about
                    profile.requirments = requirments
                    profile.gender = gender
                    db.session.commit()
                    flash('تم تحديث الملف الشخصي بنجاح')
                    return redirect(url_for('home'))
                else:
                    # Create new profile
                    new_profile = Profile(
                        nationality=nationality,
                        age=age,
                        length=length,
                        weight=weight,
                        color=color,
                        jobstatus=jobstatus,
                        qabila=qabila,
                        smokingstatus=smokingstatus,
                        martialstatus=martialstatus,
                        area=area,
                        city=city,
                        origin=origin,
                        qualifications=qualifications,
                        marriagetype=marriagetype,
                        anothernationality=anothernationality,
                        about=about,
                        requirments=requirments,
                        userid=session['userid'],
                        gender=gender
                    )
                    db.session.add(new_profile)
                    db.session.commit()
                    flash('تم إنشاء الملف الشخصي بنجاح')
                    return redirect(url_for('home'))
            
            # Handle profile deletion
            elif 'Delete' in request.form:
                if profile:
                    db.session.delete(profile)
                    db.session.commit()
                    flash('تم حذف الملف الشخصي بنجاح')
                return redirect(url_for('home'))
            
            return redirect(url_for('home'))
        
        # GET request - Initialize profile data with default values
        profile_data = {
            'nationality': '',
            'age': 18,
            'length': 160,
            'weight': 70,
            'color': '',
            'jobstatus': '',
            'qabila': '',
            'smokingstatus': 1,
            'martialstatus': 'أعزب',
            'area': '',
            'city': '',
            'origin': '',
            'qualifications': 'ثانوي',
            'marriagetype': '',
            'anothernationality': 1,
            'about': '',
            'requirments': '',
            'gender': 'ذكر'
        }
        
        # If profile exists, override defaults with actual data
        if profile:
            profile_data = {
                'nationality': profile.nationality or '',
                'age': profile.age or 18,
                'length': profile.length or 160,
                'weight': profile.weight or 70,
                'color': profile.color or '',
                'jobstatus': profile.jobstatus or '',
                'qabila': profile.qabila or '',
                'smokingstatus': profile.smokingstatus if profile.smokingstatus is not None else 1,
                'martialstatus': profile.martialstatus or 'أعزب',
                'area': profile.area or '',
                'city': profile.city or '',
                'origin': profile.origin or '',
                'qualifications': profile.qualifications or 'ثانوي',
                'marriagetype': profile.marriagetype or '',
                'anothernationality': profile.anothernationality if profile.anothernationality is not None else 1,
                'about': profile.about or '',
                'requirments': profile.requirments or '',
                'gender': profile.gender or 'ذكر'
            }
        
        # Create a dictionary with user information for the template
        user_info = {
            'fullname': user.fullname,
            'phoneno': user.phoneno
        }
        
        return render_template('profile.html', account=user_info, data=profile_data)
    
    # User is not logged in
    return redirect(url_for('login'))

@app.route('/requests')
def requests():
    # Check if user is logged in
    if 'loggedin' in session:
        # Get all requests for the current user
        user_requests = Request.query.filter_by(idtarget=session['userid']).all()
        alldata = []
        
        for req in user_requests:
            requester = User.query.get(req.idrequester)
            requester_profile = Profile.query.filter_by(userid=req.idrequester).first()
            
            if requester and requester_profile:
                request_data = {
                    'idrequest': req.idrequest,
                    'idrequester': req.idrequester,
                    'idtarget': req.idtarget,
                    'fullname': requester.fullname,
                    'phoneno': requester.phoneno,
                    'nationality': requester_profile.nationality,
                    'age': requester_profile.age,
                    'length': requester_profile.length,
                    'weight': requester_profile.weight,
                    'color': requester_profile.color,
                    'jobstatus': requester_profile.jobstatus,
                    'qabila': requester_profile.qabila,
                    'smokingstatus': requester_profile.smokingstatus,
                    'martialstatus': requester_profile.martialstatus,
                    'area': requester_profile.area,
                    'city': requester_profile.city,
                    'origin': requester_profile.origin,
                    'qualifications': requester_profile.qualifications,
                    'marriagetype': requester_profile.marriagetype,
                    'anothernationality': requester_profile.anothernationality,
                    'about': requester_profile.about,
                    'requirments': requester_profile.requirments,
                    'gender': requester_profile.gender
                }
                alldata.append(request_data)
        
        return render_template('requests.html', requests=alldata)
    
    # User is not logged in, redirect to login page
    return redirect(url_for('login'))

@app.route('/users')
def users():
    # Check if user is logged in
    if 'loggedin' in session:
        # Get all users
        all_users = User.query.all()
        return render_template('users.html', users=all_users)
    
    # User is not logged in, redirect to login page
    return redirect(url_for('login'))

@app.route('/export/<tablename>')
def export(tablename):
    if 'loggedin' in session:
        if tablename == 'users':
            data = User.query.all()
            df = pd.DataFrame([{
                'iduser': user.iduser,
                'fullname': user.fullname,
                'phoneno': user.phoneno
            } for user in data])
        elif tablename == 'profiles':
            data = Profile.query.all()
            df = pd.DataFrame([{
                'idprofile': profile.idprofile,
                'userid': profile.userid,
                'nationality': profile.nationality,
                'age': profile.age,
                'length': profile.length,
                'weight': profile.weight,
                'color': profile.color,
                'jobstatus': profile.jobstatus,
                'qabila': profile.qabila,
                'smokingstatus': profile.smokingstatus,
                'martialstatus': profile.martialstatus,
                'area': profile.area,
                'city': profile.city,
                'origin': profile.origin,
                'qualifications': profile.qualifications,
                'marriagetype': profile.marriagetype,
                'anothernationality': profile.anothernationality,
                'about': profile.about,
                'requirments': profile.requirments,
                'gender': profile.gender
            } for profile in data])
        
        output = io.StringIO()
        df.to_csv(output, index=False)
        response = make_response(output.getvalue())
        response.headers["Content-Disposition"] = f"attachment; filename={tablename}.csv"
        response.headers["Content-type"] = "text/csv"
        return response
    
    return redirect(url_for('login'))

def forgetpassword(phoneno):
    if not phoneno:
        flash('من فضلك أدخل رقم الجوال')
        return
    
    user = User.query.filter_by(phoneno=phoneno).first()
    if not user:
        flash('رقم الجوال غير موجود')
        return
    
    # Generate random password
    new_password = ''.join(choices(string.ascii_letters + string.digits, k=8))
    updatePassword(phoneno, new_password)
    
    # Send password via WhatsApp or other means
    # This would need to be implemented based on your requirements

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not old_password or not new_password or not confirm_password:
            flash('من فضلك أكمل البيانات')
            return redirect(url_for('change_password'))
        
        if new_password != confirm_password:
            flash('كلمة المرور الجديدة غير متطابقة')
            return redirect(url_for('change_password'))
        
        retcode = checkPassword(session['phoneno'], old_password)
        if retcode == 0:
            updatePassword(session['phoneno'], new_password)
            flash('تم تغيير كلمة المرور بنجاح')
            return redirect(url_for('home'))
        else:
            flash('كلمة المرور القديمة غير صحيحة')
            return redirect(url_for('change_password'))
    
    return render_template('change_password.html')

def check_db_connection(database):
    try:
        cursor = database.connection.cursor()
        cursor.execute('SELECT 1')
        return True
    except Exception as e:
        print(f"Database connection error: {e}")
        return False

# Create database tables
def create_tables():
    with app.app_context():
        db.create_all()
        # Create admin account
        create_admin()

if __name__ == '__main__':
    # Create tables before running the app
    create_tables()
    app.run(debug=True, port=5050)

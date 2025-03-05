"""
Script to generate random test data for the Dating application.
This will create random users, profiles, and match requests.
"""
from app import app, db
from models import User, Profile, MartialStatus, Request
from werkzeug.security import generate_password_hash
from faker import Faker
import random
from datetime import datetime, timedelta
import logging
import os

# Configure logging
if not os.path.exists('Logs'):
    os.makedirs('Logs')
logging.basicConfig(
    filename='Logs/test_data_generation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize Faker with Arabic locale
fake = Faker(['ar_SA'])
# Add English locale for some fields
fake_en = Faker(['en_US'])

# Constants for data generation
NATIONALITIES = ['سعودي', 'مصري', 'سوري', 'أردني', 'يمني', 'لبناني', 'فلسطيني', 'عراقي', 'كويتي', 'إماراتي']
COLORS = ['أبيض', 'أسمر', 'قمحي', 'أسمر فاتح']
JOB_STATUSES = ['موظف حكومي', 'موظف قطاع خاص', 'رجل أعمال', 'متقاعد', 'عاطل']
QABILAS = ['الدوسري', 'العتيبي', 'القحطاني', 'الشمري', 'المطيري', 'الحربي', 'العنزي', 'الرشيدي', 'البقمي', 'الزهراني']
MARITAL_STATUSES = ['أعزب', 'مطلق', 'أرمل', 'متزوج']
AREAS = ['الرياض', 'مكة المكرمة', 'المدينة المنورة', 'القصيم', 'الشرقية', 'عسير', 'تبوك', 'حائل', 'الحدود الشمالية', 'جازان']
CITIES = {
    'الرياض': ['الرياض', 'الخرج', 'الدرعية', 'الزلفي', 'المجمعة'],
    'مكة المكرمة': ['مكة', 'جدة', 'الطائف', 'رابغ', 'القنفذة'],
    'المدينة المنورة': ['المدينة', 'ينبع', 'العلا', 'المهد', 'بدر'],
    'القصيم': ['بريدة', 'عنيزة', 'الرس', 'البكيرية', 'البدائع'],
    'الشرقية': ['الدمام', 'الخبر', 'الظهران', 'الأحساء', 'القطيف'],
    'عسير': ['أبها', 'خميس مشيط', 'بيشة', 'النماص', 'محايل'],
    'تبوك': ['تبوك', 'الوجه', 'ضباء', 'تيماء', 'أملج'],
    'حائل': ['حائل', 'بقعاء', 'الغزالة', 'الشنان', 'موقق'],
    'الحدود الشمالية': ['عرعر', 'رفحاء', 'طريف', 'العويقيلة', 'جديدة عرعر'],
    'جازان': ['جازان', 'صبيا', 'أبو عريش', 'صامطة', 'الدرب']
}
QUALIFICATIONS = ['ثانوي', 'دبلوم', 'بكالوريوس', 'ماجستير', 'دكتوراه']
MARRIAGE_TYPES = ['تعدد', 'زواج عادي']
GENDERS = ['ذكر', 'أنثى']
REQUEST_STATUSES = ['pending', 'accepted', 'rejected']

def clear_database():
    """Clear all data from the database except the admin user."""
    logging.info("Clearing database")
    try:
        with app.app_context():
            # Delete all requests
            Request.query.delete()
            
            # Delete all profiles
            Profile.query.delete()
            
            # Delete all martial statuses
            MartialStatus.query.delete()
            
            # Delete all users except admin
            User.query.filter(User.phoneno != '0000000').delete()
            
            # Commit changes
            db.session.commit()
            
            logging.info("Database cleared successfully")
            print("Database cleared successfully")
    except Exception as e:
        logging.error(f"Error clearing database: {str(e)}")
        print(f"Error clearing database: {str(e)}")
        db.session.rollback()

def create_martial_statuses():
    """Create marital status entries if they don't exist."""
    logging.info("Creating marital statuses")
    for status in MARITAL_STATUSES:
        if not MartialStatus.query.filter_by(statusName=status).first():
            db.session.add(MartialStatus(statusName=status))
    db.session.commit()
    logging.info("Marital statuses created")

def generate_phone_number():
    """Generate a random Saudi phone number."""
    return f"05{random.randint(10000000, 99999999)}"

def create_users(count=50):
    """Create random users."""
    logging.info(f"Creating {count} random users")
    users = []
    for _ in range(count):
        # Generate a unique phone number
        while True:
            phone_no = generate_phone_number()
            if not User.query.filter_by(phoneno=phone_no).first():
                break
        
        # Create user
        user = User(
            fullname=fake.name(),
            password=generate_password_hash('password123', method="pbkdf2:sha256"),
            phoneno=phone_no
        )
        db.session.add(user)
        db.session.flush()  # Flush to get the user ID
        users.append(user)
        
    db.session.commit()
    logging.info(f"Created {len(users)} users")
    return users

def create_profiles(users):
    """Create profiles for users."""
    logging.info(f"Creating profiles for {len(users)} users")
    profiles = []
    for user in users:
        # Select random area and city
        area = random.choice(AREAS)
        city = random.choice(CITIES.get(area, ['Unknown']))
        
        # Create profile
        profile = Profile(
            nationality=random.choice(NATIONALITIES),
            age=random.randint(18, 60),
            length=random.randint(150, 200),  # Height in cm
            weight=random.randint(50, 120),   # Weight in kg
            color=random.choice(COLORS),
            jobstatus=random.choice(JOB_STATUSES),
            qabila=random.choice(QABILAS),
            smokingstatus=random.randint(0, 1),
            martialstatus=random.choice(MARITAL_STATUSES),
            area=area,
            city=city,
            origin=random.choice(CITIES.get(area, ['Unknown'])),
            qualifications=random.choice(QUALIFICATIONS),
            marriagetype=random.choice(MARRIAGE_TYPES),
            anothernationality=random.randint(0, 1),
            about=fake.paragraph(nb_sentences=5),
            requirments=fake.paragraph(nb_sentences=3),
            userid=user.iduser,
            gender=random.choice(GENDERS),
            created=fake.date_time_between(start_date='-1y', end_date='now')
        )
        db.session.add(profile)
        profiles.append(profile)
        
    db.session.commit()
    logging.info(f"Created {len(profiles)} profiles")
    return profiles

def create_requests(profiles, count=100):
    """Create random match requests between profiles."""
    logging.info(f"Creating {count} random match requests")
    requests_created = 0
    
    # Get all male and female profiles
    male_profiles = [profile for profile in profiles if profile.gender == 'ذكر']
    female_profiles = [profile for profile in profiles if profile.gender == 'أنثى']
    
    # If we don't have both genders, we can't create requests
    if not male_profiles or not female_profiles:
        logging.warning("Not enough profiles of both genders to create requests")
        return
    
    for _ in range(count):
        # Select random requester (male) and target (female)
        requester = random.choice(male_profiles)
        target = random.choice(female_profiles)
        
        # Skip if request already exists
        existing_request = Request.query.filter_by(
            idrequester=requester.idprofile, 
            idtarget=target.idprofile
        ).first()
        
        if existing_request:
            continue
        
        # Create request with random date in the past year
        request_date = fake.date_time_between(start_date='-1y', end_date='now')
        status = random.choice(REQUEST_STATUSES)
        
        request = Request(
            idrequester=requester.idprofile,
            idtarget=target.idprofile,
            requestdate=request_date,
            status=status
        )
        db.session.add(request)
        requests_created += 1
        
        # Commit every 10 requests to avoid large transactions
        if requests_created % 10 == 0:
            db.session.commit()
    
    db.session.commit()
    logging.info(f"Created {requests_created} match requests")

def main():
    """Main function to generate test data."""
    logging.info("Starting test data generation")
    
    try:
        with app.app_context():
            # Ask user for confirmation before clearing the database
            print("This script will clear all existing data in the database except the admin user.")
            print("Do you want to proceed? (y/n)")
            response = input().lower()
            if response != 'y':
                print("Test data generation cancelled.")
                return
            
            # Clear the database
            clear_database()
            
            # Create marital statuses
            create_martial_statuses()
            
            # Create users
            users = create_users(50)
            
            # Create profiles
            profiles = create_profiles(users)
            
            # Create requests
            create_requests(profiles, 100)
            
            logging.info("Test data generation completed successfully")
            print("Test data generation completed successfully!")
            
    except Exception as e:
        logging.error(f"Error generating test data: {str(e)}")
        print(f"Error generating test data: {str(e)}")

if __name__ == "__main__":
    main()

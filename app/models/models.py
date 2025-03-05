from datetime import datetime
import enum
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Gender(enum.Enum):
    """Enum for gender options."""
    MALE = 'MALE'
    FEMALE = 'FEMALE'

class SmokingStatus(enum.Enum):
    """Enum for smoking status options."""
    NON_SMOKER = 0
    SMOKER = 1

class User(db.Model):
    """
    User model representing the 'user' table in the database.
    Contains basic user information like name, password, and phone number.
    """
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    fullname = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(45), nullable=False, unique=True, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationships
    profiles = db.relationship('Profile', backref='user', lazy=True, cascade="all, delete-orphan")
    
    def set_password(self, password):
        """
        Set the password hash for the user.
        
        Args:
            password (str): The password to hash
        """
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Check if the provided password matches the stored hash.
        
        Args:
            password (str): The password to check
            
        Returns:
            bool: True if the password matches, False otherwise
        """
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<User {self.fullname}>'

class Profile(db.Model):
    """
    Profile model representing the 'profile' table in the database.
    Contains profile information for users.
    """
    __tablename__ = 'profile'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    nationality = db.Column(db.String(45), index=True)
    age = db.Column(db.Integer, index=True)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    skin_color = db.Column(db.String(45))
    job_status = db.Column(db.String(255))
    tribe = db.Column(db.String(45))
    smoking_status = db.Column(db.Enum(SmokingStatus))
    marital_status_id = db.Column(db.Integer, db.ForeignKey('marital_status.id'))
    area = db.Column(db.String(45))
    city = db.Column(db.String(45), index=True)
    origin = db.Column(db.String(45))
    qualifications = db.Column(db.String(45))
    marriage_type = db.Column(db.String(45))
    another_nationality = db.Column(db.Boolean, default=False)
    about = db.Column(db.Text)
    requirements = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False, index=True)
    
    # Relationships
    sent_requests = db.relationship('Request', 
                                   foreign_keys='Request.requester_id',
                                   backref='requester', 
                                   lazy=True,
                                   cascade="all, delete-orphan")
    received_requests = db.relationship('Request', 
                                       foreign_keys='Request.target_id',
                                       backref='target', 
                                       lazy=True,
                                       cascade="all, delete-orphan")
    marital_status = db.relationship('MaritalStatus', backref='profiles')
    
    def __repr__(self):
        return f'<Profile {self.id}>'

class MaritalStatus(db.Model):
    """
    MaritalStatus model representing the 'marital_status' table in the database.
    Contains different marital status options.
    """
    __tablename__ = 'marital_status'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    status_name = db.Column(db.String(45), nullable=False, unique=True)
    
    def __repr__(self):
        return f'<MaritalStatus {self.status_name}>'

class Request(db.Model):
    """
    Request model representing the 'request' table in the database.
    Contains information about match requests between users.
    """
    __tablename__ = 'request'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    target_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    request_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(45), index=True)
    
    def __repr__(self):
        return f'<Request {self.id}>'

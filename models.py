from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    """
    User model representing the 'user' table in the database.
    Contains basic user information like name, password, and phone number.
    """
    __tablename__ = 'user'
    
    iduser = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    fullname = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    phoneno = db.Column(db.String(45), nullable=False, unique=True)
    
    # Relationships
    profiles = db.relationship('Profile', backref='user', lazy=True)
    
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
    
    idprofile = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    nationality = db.Column(db.String(45))
    age = db.Column(db.Integer)
    length = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    color = db.Column(db.String(45))
    jobstatus = db.Column(db.String(255))
    qabila = db.Column(db.String(45))
    smokingstatus = db.Column(db.SmallInteger)
    martialstatus = db.Column(db.String(45))
    area = db.Column(db.String(45))
    city = db.Column(db.String(45))
    origin = db.Column(db.String(45))
    qualifications = db.Column(db.String(45))
    marriagetype = db.Column(db.String(45))
    anothernationality = db.Column(db.SmallInteger)
    about = db.Column(db.Text)
    requirments = db.Column(db.Text)
    userid = db.Column(db.Integer, db.ForeignKey('user.iduser'), nullable=False)
    gender = db.Column(db.String(45), nullable=False)
    
    # Relationships
    sent_requests = db.relationship('Request', 
                                   foreign_keys='Request.idrequester',
                                   backref='requester', 
                                   lazy=True)
    received_requests = db.relationship('Request', 
                                       foreign_keys='Request.idtarget',
                                       backref='target', 
                                       lazy=True)
    
    def __repr__(self):
        return f'<Profile {self.idprofile}>'


class MartialStatus(db.Model):
    """
    MartialStatus model representing the 'martialstatus' table in the database.
    Contains different marital status options.
    """
    __tablename__ = 'martialstatus'
    
    idmartialstatus = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    statusName = db.Column(db.String(45), nullable=False, unique=True)
    
    def __repr__(self):
        return f'<MartialStatus {self.statusName}>'


class Request(db.Model):
    """
    Request model representing the 'request' table in the database.
    Contains information about match requests between users.
    """
    __tablename__ = 'request'
    
    idmatch = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    idrequester = db.Column(db.Integer, db.ForeignKey('profile.idprofile'), nullable=False)
    idtarget = db.Column(db.Integer, db.ForeignKey('profile.idprofile'), nullable=False)
    requestdate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(45))
    
    def __repr__(self):
        return f'<Request {self.idmatch}>'

# Add any model classes for Flask-SQLAlchemy here
from . import db
from werkzeug.security import generate_password_hash

# class Post(db.Model):
class Post(db.Model):
     __tablename__ = 'post'
     id = db.Column(db.Integer, primary_key=True)
     caption= db.Column(db.String(255))
     photo = db.Column(db.String(255))
     user_id = db.Column(db.Integer)
     created_on = db.Column(db.DateTime)
    
     def __init__(self, caption, photo, user_id, created_on):
        self.caption=caption
        self.photo=photo
        self.user_id=user_id
        self.created_on = created_on

# class Likes(db.Model):
class Likes(db.Model):
     __tablename__ = 'likes'
     id = db.Column(db.Integer, primary_key=True)
     post_id = db.Column(db.Integer)
     user_id = db.Column(db.Integer)
     
     def __init__(self,post_id,user_id):
        self.post_id=post_id
        self.user_id = user_id

class Follows(db.Model):
     __tablename__ = 'follows'
     id = db.Column(db.Integer, primary_key=True)
     followers_id = db.Column(db.Integer)
     user_id = db.Column(db.Integer)

     def __init__(self,followers_id,user_id):
        self.followers_id=followers_id
        self.user_id = user_id

# class Users(db.Model):
class UserProfile(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(128))
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(128), unique=True)
    location = db.Column(db.String(128))
    biography = db.Column(db.String(255))
    profile_photo = db.Column(db.String(255))
    joined_on = db.Column(db.DateTime)
 
    def __init__(self, username, password, firstname, lastname, email,location,biography,profile_photo,joined_on):
        self.username=username
        self.password=generate_password_hash(password, method='pbkdf2:sha256')
        self.firstname=firstname
        self.lastname=lastname
        self.email=email
        self.location=location
        self.biography=biography
        self.profile_photo=profile_photo
        self.joined_on=joined_on
        
def is_authenticated(self):
        return True

def is_active(self):
        return True

def is_anonymous(self):
        return False

def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

def __repr__(self):
        return '<UserProfile %r>' % (self.username)
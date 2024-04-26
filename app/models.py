# Add any model classes for Flask-SQLAlchemy here
from . import db
import datetime
from werkzeug.security import generate_password_hash

class Users(db.Model):
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    location = db.Column(db.String(250))
    biography = db.Column(db.String(250))
    profile_photo = db.Column(db.String(100))
    joined_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    
    def __init__(self, username, password, first_name, last_name, 
                 email, location, biography, profile_photo):
        
        self.username = username
        self.password = generate_password_hash(password, method="sha256")
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.location = location
        self.biography = biography
        self.profile_photo = profile_photo
        

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
        return '<User %r>' % (self.username)
    

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(2000))
    photo = db.Column(db.String(250))
    user_id = db.Column(db.Integer)
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, caption, photo, user_id):
        self.caption = caption
        self.photo = photo
        self.user_id = user_id

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<post: %r>' % (self.id)
    
class Likes(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

    def __init__(self, post_id, user_id):
        self.post_id = post_id
        self.user_id = user_id

class Follow(db.Model):
    __tablename__ = 'follow'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    target_id = db.Column(db.Integer)


    def __init__(self, user_id, target_id):
        self.user_id = user_id
        self.target_id = target_id

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
        return '<Follows %r>' % (self.id)
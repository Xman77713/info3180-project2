# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, NumberRange
from wtforms import IntegerField, PasswordField, StringField, TextAreaField
from flask_wtf.file import FileAllowed, FileRequired, FileField

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

    firstname= StringField('First Name', validators=[InputRequired()])
    lastname=StringField('Lastname', validators=[InputRequired()])
    email=StringField('Email', validators=[InputRequired()])
    location=StringField('Location', validators=[InputRequired()])
    biography=StringField('Biography', validators=[InputRequired()])
    
    profile_photo = FileField('Photo', validators=[
    FileRequired(),
    FileAllowed(['jpg', 'png'], 'Images only!')])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class PostForm(FlaskForm):
    caption = StringField('caption', validators=[InputRequired()])
    photo = FileField('Photo', validators=[
    FileRequired(),
    FileAllowed(['jpg', 'png'], 'Images only!')])
    user_id=IntegerField('User ID', validators=[InputRequired(), NumberRange(min=1)])
    
# class UploadForm(FlaskForm):
#     photo = FileField('Photo', validators=[
#     FileRequired(),
#     FileAllowed(['jpg', 'png'], 'Images only!')])
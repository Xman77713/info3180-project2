from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired
from flask_wtf.file import FileAllowed, FileRequired, FileField 

class SignupForm(FlaskForm):
    phone_num = StringField('Phone#', validators=[InputRequired()])
    fullname = StringField('Fullname', validators=[InputRequired()])
    username1 = StringField('Username', validators=[InputRequired()])
    password1 = PasswordField('Password', validators=[InputRequired()])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class UploadForm(FlaskForm):
    photo = FileField('Photo', validators=[
    FileRequired(),
    FileAllowed(['jpg', 'png','gif','mp4'],'Upload a photo or Video')])
    caption = StringField('Caption')
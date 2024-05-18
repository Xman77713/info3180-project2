"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, jsonify, send_file, session, send_from_directory
import os
from functools import wraps
from werkzeug.security import check_password_hash
from app.models import Post, Likes, Follows, UserProfile
from app.forms import RegisterForm, LoginForm, PostForm
from flask_wtf.csrf import generate_csrf
from werkzeug.utils import secure_filename
import datetime
import jwt

###
# Routing for your application.
###

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not 'Authorization' in request.headers:
            return jsonify({"error": "Incorrent token!"}), 400
        token = request.headers['Authorization'].split()[1]
        try:
            token = jwt.decode(
                token,
                app.config['SECRET_KEY'],
                'HS256'
            )
        except Exception as e:
            return jsonify({"error": "Please Login before proceeding"}), 400
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    return jsonify(message="Share photos of your favourite moments with friends, family and the world.")

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})

# API ROUTES

@app.route('/api/v1/register', methods=['POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Gather data from the form
        username = form.username.data
        password = form.password.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        
        errors = []
        existing_email = db.session.execute(db.select(UserProfile).filter_by(email=email)).scalar()
        if existing_email:
            errors.append("Email already exists")

        existing_username = db.session.execute(db.select(UserProfile).filter_by(username=username)).scalar()
        if existing_username:
            errors.append("Username already exists")
        
        if errors != []:
            return jsonify({"errors":errors}), 400

        location = form.location.data
        biography = form.biography.data
        profile_photo = form.profile_photo.data
        filename = secure_filename(profile_photo.filename)

        profile_photo.save(
            os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename)
        )

        joined_on = datetime.datetime.now()

        user = UserProfile(
            username,
            password,
            firstname,
            lastname,
            email,
            location,
            biography,
            filename,
            joined_on
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({"message":"Successfully created account"}), 201
    else:
        return jsonify({"errors":form_errors(form)}), 400

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = db.session.execute(db.select(UserProfile).filter_by(username=username)).scalar()
        print(user)
        if not user or not check_password_hash(user.password, password):
            return jsonify({'errors':'Invalid username or password'}), 401
        token = jwt.encode({'user_id':user.id}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token':token})
    else:
        return jsonify({"errors": form_errors(form)}), 400

@app.route('/api/v1/auth/logout', methods=['POST'])
def logout():
    return jsonify({'message':'Logged out successfully'})

@app.route('/api/v1/users/<user_id>/posts', methods=['GET', 'POST'])
@token_required
def user_posts(user_id):
    form = PostForm()
    if request.method == 'GET':
        message = None
        token = request.headers['authorization'].split()[1]
        token = jwt.decode(token, app.config['SECRET_KEY'], 'HS256')
        posts = db.session.execute(db.select(Post.photo).filter_by(user_id=user_id)).all()
        if posts == []:
            message = "There are no posts to view"
            posts = None      
            posts_count = "0"
        else:
            posts = [{'photo':"/api/v1/posts/"+post.photo} for post in posts]
            posts_count = str(len(posts))

        user = db.session.execute(db.select(UserProfile).filter_by(id=user_id)).scalar()

        followers = len(db.session.execute(db.select(Follows).filter_by(user_id=user_id)).all())

        return jsonify({
            "message":message,
            "posts":posts,
            "user":{
                "firstname":user.firstname,
                "lastname":user.lastname,
                "location":user.location,
                "joined_on":user.joined_on.strftime("%B %Y"),
                "biography":user.biography,
                "profile_photo":"/api/v1/users/"+user.profile_photo,
                "postcount":posts_count},
            "followers":followers,
            "followed":True if db.session.execute(db.select(Follows).filter_by(user_id=user_id,followers_id=token['user_id'])).scalar() else False
        })
    elif form.validate_on_submit():
        caption = form.caption.data
        photo = form.photo.data
        filename = secure_filename(photo.filename)

        photo.save(
            os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename)
        )

        post = Post(caption=caption, 
                    photo=filename, 
                    user_id=user_id, 
                    created_on=datetime.datetime.now())
        db.session.add(post)
        db.session.commit()

        return jsonify({'message': 'Post created successfully'}), 201
    else:
        return jsonify({"errors": form_errors(form)}), 400

@app.route('/api/v1/posts', methods=['GET'])
@token_required
def get_all_post(): #TODO: Not completed
    posts = db.session.execute(db.select(Post)).scalars()
    token = request.headers['authorization'].split()[1]
    token = jwt.decode(token, app.config['SECRET_KEY'], 'HS256')

    if not posts:
        return jsonify({"error":"There are no posts to view"}), 200
    else:
        posts = [{
            "username":str(db.session.execute(db.select(UserProfile.username).filter_by(id=post.user_id)).scalar()),
            "profilePhoto":"/api/v1/users/"+db.session.execute(db.select(UserProfile.profile_photo).filter_by(id=post.user_id)).scalar(),
            "caption":post.caption, 
            "photo":"/api/v1/posts/"+post.photo, 
            "user_id":post.user_id, 
            "id":post.id,
            "liked":
            True if db.session.execute(db.select(Likes).filter_by(user_id=token['user_id'], post_id=post.id)).scalar() else False,
            "likes":len(db.session.execute(db.select(Likes.post_id).filter_by(post_id=post.id)).all()),
            "created_on":post.created_on.strftime("%d %b %Y")} for post in posts]
        for post in posts: print(post)
        return jsonify({"posts": posts}), 200

@app.route('/api/v1/posts/<post_id>/like')
def likepost(post_id): #TODO: Not yet used
    print(post_id)
    token = request.headers['authorization'].split()[1]
    token = jwt.decode(token, app.config['SECRET_KEY'], 'HS256')
    like = db.session.execute(db.select(Likes).filter_by(post_id=post_id, user_id=token['user_id'])).scalar()

    if not like:
        like = Likes(post_id=post_id, user_id=token['user_id'])
        db.session.add(like)
        db.session.commit()
        likes = len(db.session.execute(db.select(Likes).filter_by(post_id=post_id)).all())
        return jsonify({
            'message': 'Post liked successfully',
            'likes':likes,
            'liked':True})
    else:
        db.session.delete(like)
        db.session.commit()
        likes = len(db.session.execute(db.select(Likes).filter_by(post_id=post_id)).all())
        return jsonify({
            'message': 'Post unlike successfully',
            'likes':likes,
            'liked':False})

@app.route('/api/v1/users/<user_id>/follow')
def follow_user(user_id): #TODO: not started yet
    token = request.headers['authorization'].split()[1]
    token = jwt.decode(token, app.config['SECRET_KEY'], 'HS256')

    follow = db.session.execute(db.select(Follows).filter_by(followers_id=token['user_id'], user_id=user_id)).scalar()
    if not follow:
        follow = Follows(followers_id=token['user_id'], user_id=user_id)
        db.session.add(follow)
        db.session.commit()
        followers = len(db.session.execute(db.select(Follows).filter_by(user_id=user_id)).all())
        return jsonify({
            'message': 'User followed successfully',
            'followers': followers,
            'followed':True}), 201
    else:
        db.session.delete(follow)
        db.session.commit()
        followers = len(db.session.execute(db.select(Follows).filter_by(user_id=user_id)).all())
        return jsonify({
            'message': 'User unfollowed successfully',
            'followers': followers,
            'followed':False}), 201

@app.route('/api/v1/posts/<filename>') #MAY BE USED TO FIND PICTURES, CHANGE TO FIT CURRENT CODE
def getPostImage(filename): #TODO: Used in posts, needed for userview
    return send_from_directory(os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER']),filename)

@app.route('/api/v1/users/<filename>') #MAY BE USED TO FIND PICTURES, CHANGE TO FIT CURRENT CODE
def getProfilePhoto(filename):
    return send_from_directory(os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER']),filename)

# @app.route('/api/v1/posts/')
# def getLikes():
    # return render_template('expression')

###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
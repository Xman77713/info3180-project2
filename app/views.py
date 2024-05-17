"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db, login_manager

from flask import render_template, request, redirect, url_for, flash, abort

from flask_login import login_user, logout_user, current_user, login_required

from app.forms import LoginForm, UploadForm
from app.models import users
from werkzeug.security import check_password_hash
from is_safe_url import is_safe_url


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="Home")

@app.route('/register')
def register():
    return "Registration Page"

@app.route('/register',methods=['GET','POST'])
def register():
    myform = SignupForm()

    if myform.validate_on_submit():
        phone_num = myform.phone_num.data
        fullname = myform.fullname.data
        username1 = myform.username1.data
        password1 = myform.password1.data

        flash('User registered successfully')
        return redirect(url_for('home'))
     
    return render_template("contact.html", form = myform)


@app.route('/login', methods=['GET','POST'])
def login():
    myform = LoginForm()

    if myform.validate_on_submit():
        username = myform.username.data
        password = myform.password.data

        user = db.session.execute(db.select(Users).filter_by(username=username)).scalar()


        if user is not None and check_password_hash(user.password, password):
            remember_me = False

            if 'remember_me' in request.form:
                remember_me = True
            login_user(user), remember = remember_me)

            flash('Login Successful','success')
            redirect(url_for('home'))
        
        else:
            flash('Username or Password is incorrect.','danger')
        
        flash_errors(myform)
     
    return render_template("contact.html", form = myform)

@app.route('/explore')


@app.route('/users/{user_id}')

@app.route('/posts/new')
@login_required
def posts():
    # Instantiate your form class
    form = UploadForm()

    # Validate file upload on submit
    if form.validate_on_submit():
        # Get file data and save to your uploads folder
        photo = form.photo.data
        filename = secure_filename(photo.filename)
        caption = form.caption.data
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

        flash('File Saved', 'success')
        return redirect(url_for('home')) # Update this to redirect the user to a route that displays all uploaded image files

    return render_template('upload.html',form = form)   

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logging Out...','Success')
    return redirect(url_for('home'))


@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(Users).filter_by(id=id)).scalar()

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')


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
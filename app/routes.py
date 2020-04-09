from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Exercise
from werkzeug.urls import url_parse

@app.route('/')                 # decorators; create associations between URL given and the function below
@app.route('/index')
@login_required
def index():
    user = {'username': 'Neil'}
    exercises = Exercise.query.all()
    # exercises = [
    #     {
    #         'id' : 1,
    #         'title' : 'Running',
    #         'date_time': 'Sundays 14:30',
    #         'location': 'Sgoil Lionacleit',
    #         'details' : '5km run',
    #         'contact' : 'n/a',
    #
    #     },
    #     {
    #         'id' : 2,
    #         'title' : 'Kickboxing',
    #         'date_time': 'Mondays 8 - 10pm',
    #         'location': 'Carnish Hall',
    #         'details' : 'n/a',
    #         'contact' : 'n/a',
    #     },
    #     {
    #         'id' : 3,
    #         'title' : 'Volleyball',
    #         'date_time': '? 7-9pm',
    #         'location': 'Sgoil Lionacleit',
    #         'details' : 'n/a',
    #         'contact' : 'n/a',
    #     },
    #     {
    #         'id' : 4,
    #         'title' : 'Hot Vinyasa Flow Yoga',
    #         'date_time': 'Wednesdays 6-7.45pm',
    #         'location': 'Taigh Sgire',
    #         'details' : 'aerobic',
    #         'contact' : 'Yoga for Life Hebrides',
    #     }
    # ]

    return render_template('index.html', title="Home", exercises=exercises)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/', methods=['GET', 'POST'])
@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = PostForm()
    if form.validate_on_submit():
        exercise = Exercise(title=form.title.data, date_time=form.date_time.data, location=form.location.data, details=form.details.data, contact=form.contact.data)
        db.session.add(exercise)
        db.session.commit()
        flash('Your exercise is now live!')
        return redirect(url_for('index'))
    # the following block needs revised
    exercises = Exercise.query.filter_by(id=current_user.id)
    return render_template('user.html', user=user, form=form, exercises=exercises)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

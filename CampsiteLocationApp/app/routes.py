from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, SignupForm, EditProfileForm, WriteReviewForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Review, Campsite
from werkzeug.urls import url_parse
from datetime import datetime as dt


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = dt.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/get_map')
def get_map():
    return render_template('testGoogleAPI.html')


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
        flash(f'Logged in as {user.username}')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you\'re signed up!')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Signup', form=form)


@app.route('/profile')
@login_required
def profile():
    campsites = current_user.campsites.all()
    return render_template('profile.html', user=current_user, campsites=campsites)


@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
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


@app.route('/campsites')
@login_required
def campsites():
    campsites = [
        {'name': 'CampName1', 'description': 'Test description #1'},
        {'name': 'CampName2', 'description': 'Test description #2'}
    ]
    return render_template('campsites.html', title='Campsites', campsites=campsites)


@app.route('/review/<cid>/<pid>', methods=['GET', 'POST'])
@login_required
def review(cid, pid):
    print('REVIEWING')
    form = WriteReviewForm()
    if form.validate_on_submit():
        review_body = form.review.data
        review = Review(body=review_body,
                        user_id=current_user.id,
                        contract_id=cid,
                        park_id=pid)
        db.session.add(review)
        print('SAVINGREVIEW')
        db.session.commit()
        flash(f'Review saved for campsite at {cid}: {pid}')
        return redirect(url_for('profile'))
    return render_template('review.html', cid=cid, pid=pid, form=form)
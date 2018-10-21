from flask import render_template, flash, redirect, url_for, request, session
from app import app, db
from app.forms import LoginForm, SignupForm, EditProfileForm, WriteReviewForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Review, Campsite
from werkzeug.urls import url_parse
from json import dumps
from collections import OrderedDict
import xml.etree.ElementTree as ET
import sys
from math import sin, cos, sqrt, atan2, radians
from datetime import datetime as dt


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = dt.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
def index():
    return render_template('Home.html')


@app.route('/indexRec')
def indexRec():
    return render_template('indexRec.html')


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
                    email=form.email.data,
                    fist_name=form.first_name.data,
                    last_name=form.last_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you\'re signed up!')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Signup', form=form)


@app.route('/profile')
@login_required
def profile():
    # TODO: changeback
    # campsites = current_user.favorites
    campsites = [
        {'name': 'Arcadia Campgrounds', 'img': '/static/img/Feature_01.jpg', 'description': 'Angeles Crest Creamery is a working goat dairy on 70 private acres in the Angeles National Forest. Our camp site is a natural clearing in the great state of California.'},
        {'name': 'Arcadia Campgrounds', 'img': '/static/img/Feature_01.jpg', 'description': 'Angeles Crest Creamery is a working goat dairy on 70 private acres in the Angeles National Forest. Our camp site is a natural clearing in the great state of California.'},
        {'name': 'Arcadia Campgrounds', 'img': '/static/img/Feature_01.jpg', 'description': 'Angeles Crest Creamery is a working goat dairy on 70 private acres in the Angeles National Forest. Our camp site is a natural clearing in the great state of California.'},
        {'name': 'Arcadia Campgrounds', 'img': '/static/img/Feature_01.jpg', 'description': 'Angeles Crest Creamery is a working goat dairy on 70 private acres in the Angeles National Forest. Our camp site is a natural clearing in the great state of California.'}]
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


@app.route('/campsites', methods=['GET', 'POST'])
@login_required
def campsites():
    # TODO: Replace dummmy data
    campsites = [
        {'name': 'Arcadia Campgrounds', 'img': '/static/img/Feature_01.jpg', 'description': 'Angeles Crest Creamery is a working goat dairy on 70 private acres in the Angeles National Forest. Our camp site is a natural clearing in the great state of California.'},
        {'name': 'Arcadia Campgrounds', 'img': '/static/img/Feature_01.jpg', 'description': 'Angeles Crest Creamery is a working goat dairy on 70 private acres in the Angeles National Forest. Our camp site is a natural clearing in the great state of California.'},
        {'name': 'Arcadia Campgrounds', 'img': '/static/img/Feature_01.jpg', 'description': 'Angeles Crest Creamery is a working goat dairy on 70 private acres in the Angeles National Forest. Our camp site is a natural clearing in the great state of California.'},
        {'name': 'Arcadia Campgrounds', 'img': '/static/img/Feature_01.jpg', 'description': 'Angeles Crest Creamery is a working goat dairy on 70 private acres in the Angeles National Forest. Our camp site is a natural clearing in the great state of California.'}
    ]
    return render_template('campsites.html', title='Campsites', campsites=campsites)


@app.route('/campsite/<cid>/<pid>')
def site(cid, pid):
    # TODO: fetch park data from api
    reviews = Review.query.filter_by(contract_id=cid, park_id=pid).all()
    return render_template('site.html', cid=cid, pid=pid, reviews=reviews)



@app.route('/reviews/new/<cid>/<pid>', methods=['GET', 'POST'])
@login_required
def new_review(cid, pid):
    form = WriteReviewForm()
    if form.validate_on_submit():
        review_body = form.review.data
        review = Review(body=review_body,
                        user_id=current_user.id,
                        contract_id=cid,
                        park_id=pid)
        db.session.add(review)
        db.session.commit()
        flash(f'Review saved for campsite at {cid}: {pid}')
        return redirect(url_for('profile'))
    return render_template('new_review.html', cid=cid, pid=pid, form=form)


@app.route('/campsite/<cid>/<pid>/add', methods=['POST'])
@login_required
def add_favorite(cid, pid):
    campsite = Campsite.query.filter_by(contract_id=cid, park_id=pid)
    if not campsite:
        data = request.form
        campsite = Campsite(contract_id=cid,
                            park_id=pid,
                            facility_name=data.get('name'),
                            description=data.get('description'),
                            img=data.get('img'))
    current_user.favorites.append(campsite)
    # db.session.add(current_user)
    db.session.commit()


@app.route('/api/search', methods = ['POST'])
def get_post_javascript_data():

    returndata = request.form.get('XMLCampsiteData')
    returnLocation = request.form.get('location')
    radius = request.form.get('radius')

    parsedData = XMLParse(returndata)

    CalculateNearbyCampsites(parsedData, returnLocation, radius)

    return "ok"

def XMLParse(xmldata):
    xmldata = xmldata.replace("\n", "")

    root = ET.fromstring(xmldata)

    if not root:
      return "Error in parsing XML data"

    return root

def CalculateNearbyCampsites(data, location, radius):
    temp = location.split(",")
    latitude = round(float(temp[0]))
    longitude = round(float(temp[1]))

    print("STARTING", latitude, longitude)

    print("starting count", len(data))

    count = 0

    for ele in data:
        if ele.attrib["latitude"] == "" or ele.attrib["longitude"] == "":
            continue
        targetlatitude = round(float(ele.attrib["latitude"]))
        targetlongitude = round(float(ele.attrib["longitude"]))
        print(ele.attrib["facilityName"], ele.attrib["latitude"], ele.attrib["longitude"])

        # approximate radius of earth in km
        R = 6373.0

        lati = radians(latitude)
        loni = radians(longitude)
        latf = radians(targetlatitude)
        lonf = radians(targetlongitude)

        dlon = lonf - loni
        dlat = latf - lati

        a = sin(dlat / 2) ** 2 + cos(lati) * cos(latf) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        #times conversion factor to transfer to miles
        distance = R * c * 0.621371

        if distance <= float(radius):
            print(ele.attrib["facilityName"], "is within the radius")
            count += 1

    print("finishing count: ", count)

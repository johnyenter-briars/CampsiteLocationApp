from flask import render_template, flash, redirect, url_for, request, session
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from xmljson import BadgerFish
from json import dumps
from collections import OrderedDict
import xml.etree.ElementTree as ET
import sys
from math import sin, cos, sqrt, atan2, radians


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/indexRec')
def indexRec():
    return render_template('indexRec.html')

@app.route('/get_map')
def get_map():
    return render_template('testGoogleAPI.html')


@app.route('/layout/<name>')
def profile(name):

    return render_template('layout.html', name=name)


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
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/set/')
def set():
    session['key'] = 'value'
    return 'ok'

@app.route('/getLatandLong/')
def getLatandLong():
    if session.get('LatandLong') is None:
        return "The session storage at that key returned none"
    return session.get('LatandLong')

@app.route('/getJSON/')
def getJSON():
    if session.get('json') is None:
        return "The session storage at that key returned none"
    return session.get('json')

@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():

    returndata = request.form['XMLCampsiteData']
    returnLocation = request.form['location']
    radius = request.form['radius']

    parsedData = XMLParse(returndata)

    CalculateNearbyCampsites(parsedData, returnLocation, radius)

    return "ok"

@app.route('/XMLParse/')
def XMLParse(xmldata):
    xmldata = xmldata.replace("\n", "")

    root = ET.fromstring(xmldata)
    if root is not None:
        return root;

    return "Error in parsing XML data"

@app.route('/CalculateNearbyCampsites/')
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

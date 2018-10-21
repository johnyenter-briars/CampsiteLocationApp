from flask import render_template, flash, redirect, url_for, request, session
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from xmljson import BadgerFish
from json import dumps
from collections import OrderedDict
from xml.etree.ElementTree import fromstring
import sys

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
    jsdata = request.form['javascript_data']

    return jsdata

@app.route('/XMLtoJSON/')
def XMLtoJSON(xmldata):

    bf = BadgerFish(dict_type=OrderedDict)

    data = dumps(bf.data(fromstring(xmldata)))

    return data
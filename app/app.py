#!/usr/bin/env python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask import request
from wtforms import Form, BooleanField, StringField, validators
from wtforms.validators import Required
import uuid

app = Flask(__name__)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)


db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'



@app.route("/")
def hello():
    print "hello"
    user = {'nickname': 'Miguel'}  # fake user
    return "WECLOME AT DRIVER COACH!"




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

class DailyRankings(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    score = db.Column(db.Integer)
    def __init__(id, score):
        self.id= id
        self.score = score

@app.route("/postresult", methods=['GET', 'POST'])
def postresult():
    error = None
    if request.method == 'POST':
        #//need to validate inputs!!!
        db.session.add(Rankings(request.form['id'],request.form['score']))
         #//Space the commits Efficients
        db.session.commit()

@app.route("/postresult", methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['email']):
                user = User()
                uid = generateRandomUid();
                user.id = uid
                return uid
    else:
            error = 'Invalid username/password'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        error = None
        form = LoginForm()
        validateForm()
        return render_template('login.html', error=error, form=form)


class LoginForm(Form):
    username = StringField('username', validators=[Required()])
    email = BooleanField('email', validators=[Required()])

def valid_login():
    return True

def generateRandomUid():
    uid = uuid.uuid4()
    while User.query.filter_by(id= uid).first() != None:
        uid = uuid.uuid4()

    return uid

def computeRnakings():
    min_score = -1*db.func.max(Rankings.score).scalar()
    candidates = Rankings.query.all()
    for row in Rankings.query.all():
        row.score += min_score
        db.session.add(row)
        db.session.commit()

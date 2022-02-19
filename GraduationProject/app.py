from flask import Flask, render_template, url_for,jsonify, redirect, flash, session,request
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_mail import Message, Mail
from werkzeug.security import generate_password_hash, check_password_hash

from form import *

from config import Config
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    email = session.get('EMAIL')
    name = session.get('NAME')
    return render_template('index.html', email=email, name=name)


app.config["MAIL_SERVER"] = 'smtp.qq.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = '1575631865@qq.com'
app.config['MAIL_PASSWORD'] = 'tdquheqqcyuhidcf'
app.config['MAIL_DEFAULT_SENDER'] = '1575631865@qq.com'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

s = URLSafeTimedSerializer('Thisiaas')
mail = Mail(app)

import requests

@app.route('/email_verification', methods=['GET', 'POST'])
def email_varification():
    form = EmailVeriForm()
    if form.validate_on_submit():
        email = form.email.data
        user_in_db = Student.query.filter(Student.student_email == email).first()
        print('hello')
        if not user_in_db:
            token = s.dumps(email, salt='email-confirm')
            # Access API to verify your email address
            # url = 'http://apilayer.net/api/check?access_key=e1d7174635e48945b8ff1b6bb5b5b789&email='+email+'&smtp=1&format=1'
            # r = requests.get(url)
            # print(r.json())
            # if r.json()['smtp_check'] == True:
            if True:
                msg = Message('Confirm Email', sender='1575631865@qq.com', recipients=[email])
                link = url_for('signup', token=token, _external=True)
                msg.body = 'Click to finish your registeration: {}'.format(link)
                mail.send(msg)
                flash('Please check your Email, and follow the email link')
            else:
                flash('This is not a valid email')
        else:
            flash('This Email Has Been Registered')
        session['EMAIL'] = email
    return render_template('email_verification.html',form=form)


@app.route('/signup/<token>', methods=['GET', 'POST'])
def signup(token):
    form = SignupForm()
    try:
        email = s.loads(token, salt='email-confirm', max_age=180)
        if form.validate_on_submit():
            if form.firstname.data.isalpha() and form.lastname.data.isalpha():
                passw_hash = generate_password_hash(form.password.data)
                student = Student(student_email=session.get('EMAIL'), student_firstname=form.firstname.data, student_lastname=form.lastname.data,
                                   student_password=passw_hash,student_gender=form.gender.data,student_phone=form.phone.data,
                                  student_level=form.level.data,
                                   student_school=form.school.data,student_dob=form.dob.data,student_address=form.address.data)
                db.session.add(student)
                db.session.commit()
                session.clear()
                return redirect(url_for('signin'))
            else:
                flash('Your name could only contain letter of alphabet')
    except SignatureExpired:
        flash('Token is expired, please resend an email to sign up')
    return render_template('signup.html', form=form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        psw = form.password.data
        user_in_db = Student.query.filter(Student.student_email == form.email.data).first()
        if user_in_db:
            if check_password_hash(user_in_db.student_password, psw):
                print('Login Success')
                session['NAME'] = user_in_db.student_firstname
                session['EMAIL'] = user_in_db.student_email
                session['ACTOR'] = 'Student'
                return redirect(url_for("index"))
            else:
                flash('Incorrect password')
                return redirect(url_for("signin"))
        else:
            flash('No user found')
            return redirect(url_for("signin"))
    return render_template('signin.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

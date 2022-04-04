import base64
import os
import wolframalpha
from mathgenerator import mathgen

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


# app name
@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
    # defining function
    return render_template("404.html")


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    email = session.get('EMAIL')
    # user_type = session.get('ACTOR')
    # name = ''
    # if email and user_type == 'Student':
    #     student = Student.query.filter(Student.student_email == email).first()
    #     name = student.student_firstname
    name = session.get('NAME')
    print(name)
    # session['NAME'] = name
    # session['ACTOR'] = 'Student'
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
        if not user_in_db:
            token = s.dumps(email, salt='email-confirm')
            # Access API to verify your email address
            # url = 'http://apilayer.net/api/check?access_key=e1d7174635e48945b8ff1b6bb5b5b789&email='+email+'&smtp=1&format=1'
            # r = requests.get(url)
            # print(r.json())
            # if r.json()['smtp_check'] == True:
            if True:
                msg = Message('Just Math it - Sign up Email', sender='1575631865@qq.com', recipients=[email])
                link = url_for('signup', token=token, _external=True)
                msg.body = 'Click to finish your sign up: {}'.format(link)
                mail.send(msg)
                flash('Please check your Email, and follow the email link to finish your sign up')
            else:
                flash('This is not a valid email')
        else:
            flash('This Email has been registered')
        session['EMAIL'] = email
    return render_template('email_verification.html',form=form)


@app.route('/teacher_email_verification', methods=['GET', 'POST'])
def teacher_email_verification():
    form = TeacherEmailVeriForm()
    if form.validate_on_submit() and form.token.data == '123':
        email = form.email.data
        user_in_db = Teacher.query.filter(Teacher.teacher_email == email).first()
        if not user_in_db:
            token = s.dumps(email, salt='email-confirm')
            # Access API to verify your email address
            # url = 'http://apilayer.net/api/check?access_key=e1d7174635e48945b8ff1b6bb5b5b789&email='+email+'&smtp=1&format=1'
            # r = requests.get(url)
            # print(r.json())
            # if r.json()['smtp_check'] == True:
            if True:
                msg = Message('Just Math it - Sign up Email', sender='1575631865@qq.com', recipients=[email])
                link = url_for('signup_teacher', token=token, _external=True)
                msg.body = 'Click to finish your sign up: {}'.format(link)
                mail.send(msg)
                flash('Please check your Email, and follow the email link to finish your sign up as a teacher')
            else:
                flash('This is not a valid email')
        else:
            flash('This Email has been registered')
        session['EMAIL'] = email
    elif form.token.data != '123':
        flash('The token is not correct')
    return render_template('teacher_email_verification.html',form=form)


@app.route('/change_pass_verification', methods=['GET', 'POST'])
def change_pass_verification():
    form = EmailVeriForm()
    if form.validate_on_submit():
        email = form.email.data
        student_in_db = Student.query.filter(Student.student_email == email).first()
        teacher_in_db = Teacher.query.filter(Teacher.teacher_email == email).first()
        if student_in_db:
            token = s.dumps(email, salt='email-confirm')
            # Access API to verify your email address
            # url = 'http://apilayer.net/api/check?access_key=e1d7174635e48945b8ff1b6bb5b5b789&email='+email+'&smtp=1&format=1'
            # r = requests.get(url)
            # print(r.json())
            # if r.json()['smtp_check'] == True:
            if True:
                token = s.dumps(email, salt='email-confirm')
                msg = Message('Just Math it - Modify your password', sender='1575631865@qq.com', recipients=[email])
                link = url_for('change_password', token=token, _external=True)
                msg.body = 'Click to change your password: {}'.format(link)
                mail.send(msg)
                session['ACTOR'] = 'Student'
                flash('Please check your Email, and follow the email link to modify your password')
            else:
                flash('This is not a valid email')
        elif teacher_in_db:
            token = s.dumps(email, salt='email-confirm')
            # Access API to verify your email address
            # url = 'http://apilayer.net/api/check?access_key=e1d7174635e48945b8ff1b6bb5b5b789&email='+email+'&smtp=1&format=1'
            # r = requests.get(url)
            # print(r.json())
            # if r.json()['smtp_check'] == True:
            if True:
                token = s.dumps(email, salt='email-confirm')
                msg = Message('Just Math it - Modify your password', sender='1575631865@qq.com', recipients=[email])
                link = url_for('change_password', token=token, _external=True)
                msg.body = 'Click to change your password: {}'.format(link)
                mail.send(msg)
                session['ACTOR'] = 'Teacher'
                flash('Please check your Email, and follow the email link to modify your password')
            else:
                flash('This is not a valid email')
        else:
            flash('Sorry! Your have not got an account, please sign up a new one!')
        session['EMAIL'] = email
    return render_template('change_pass_verification.html',form=form)


@app.route('/change_password/<token>', methods=['GET', 'POST'])
def change_password(token):
    from models import db
    form = ChangePassword()
    user_type = session.get('ACTOR')
    print(user_type)
    try:
        email = s.loads(token, salt='email-confirm', max_age=180)
        if form.validate_on_submit() and user_type == 'Student':
            student = Student.query.filter(Student.student_email == session.get('EMAIL')).first()
            student.student_password = generate_password_hash(form.password.data)
            db.session.add(student)
            db.session.commit()
            session.clear()
            flash("Change successfully")
            return redirect(url_for('signin'))
        elif form.validate_on_submit() and user_type == 'Teacher':
            teacher = Teacher.query.filter(Teacher.teacher_email == session.get('EMAIL')).first()
            teacher.teacher_password = generate_password_hash(form.password.data)
            db.session.add(teacher)
            db.session.commit()
            session.clear()
            flash("Change successfully")
            return redirect(url_for('signin'))
        elif user_type is None:
            flash('Please use the same browser on the same computer to finish password change. Otherwise, this will '
                  'not work.')
    except SignatureExpired:
        flash('Token is expired, please resend an email to sign up')
    return render_template('change_password.html', form=form)


@app.route('/signup/<token>', methods=['GET', 'POST'])
def signup(token):
    form = SignupForm()
    try:
        email = s.loads(token, salt='email-confirm', max_age=180)
        if form.validate_on_submit():
            if form.firstname.data.isalpha() and form.lastname.data.isalpha():
                passw_hash = generate_password_hash(form.password.data)
                student = Student(student_email=email, student_firstname=form.firstname.data, student_lastname=form.lastname.data,
                                   student_password=passw_hash,student_gender=form.gender.data,student_phone=form.phone.data,
                                   student_school=form.school.data,student_dob=form.dob.data,student_address=form.address.data)
                db.session.add(student)
                db.session.commit()
                session.clear()
                flash('Sign up successfully')
                return redirect(url_for('signin'))
            else:
                flash('Your name could only contain letter of alphabet')
    except SignatureExpired:
        flash('Token is expired, please resend an email to sign up')
    return render_template('signup.html', form=form)


@app.route('/signup_teacher/<token>', methods=['GET', 'POST'])
def signup_teacher(token):
    form = TeacherSignupForm()
    try:
        email = s.loads(token, salt='email-confirm', max_age=180)
        if form.validate_on_submit():
            if form.firstname.data.isalpha() and form.lastname.data.isalpha():
                passw_hash = generate_password_hash(form.password.data)
                teacher = Teacher(teacher_email=email, teacher_firstname=form.firstname.data, teacher_lastname=form.lastname.data,
                                   teacher_password=passw_hash,teacher_phone=form.phone.data,
                                   teacher_school=form.school.data)
                db.session.add(teacher)
                db.session.commit()
                session.clear()
                flash('Sign up successfully')
                return redirect(url_for('signin'))
            else:
                flash('Your name could only contain letter of alphabet')
    except SignatureExpired:
        flash('Token is expired, please resend an email to sign up')
    return render_template('signup_teacher.html', form=form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        psw = form.password.data
        student_in_db = Student.query.filter(Student.student_email == form.email.data).first()
        teacher_in_db = Teacher.query.filter(Teacher.teacher_email == form.email.data).first()
        if student_in_db:
            if check_password_hash(student_in_db.student_password, psw):
                print('Login Success')
                session['NAME'] = student_in_db.student_firstname
                session['EMAIL'] = student_in_db.student_email
                session['ACTOR'] = 'Student'
                return redirect(url_for("index"))
            else:
                flash('Incorrect password')
                return redirect(url_for("signin"))
        elif teacher_in_db:
            if check_password_hash(teacher_in_db.teacher_password, psw):
                print('Login Success')
                session['NAME'] = teacher_in_db.teacher_firstname
                session['EMAIL'] = teacher_in_db.teacher_email
                session['ACTOR'] = 'Teacher'
                return redirect(url_for("index"))
            else:
                flash('Incorrect password')
                return redirect(url_for("signin"))
        else:
            flash('No user found')
            return redirect(url_for("signin"))
    return render_template('signin.html', form=form)


@app.route('/topics/<topic>/', methods=['GET', 'POST'])
def topics(topic):
    name = session.get('NAME')
    topic_ = Topics.query.filter(Topics.topic_name == topic).first()
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 3))
    paginate = Skills.query.filter(Skills.topic_id == topic_.topic_id).paginate(page, per_page, error_out=False)
    comments = []
    skills = paginate.items
    for skill in skills:
        comments.append(Comments.query.filter(Comments.skill_id == skill.skill_id).count())
    # app_id = 'XQAUEU-WR3AY23332'
    # client = wolframalpha.Client(app_id)
    # problem, solution = mathgen.genById(4)
    # if (len(problem.split("Equation")) > 1):
    #     problem = problem.split("Equation")[1]
    # res = client.query('Convert 21421 from base 10 to base 7.')
    # # img_list = []
    # for pod in res.pods:
    #     for sub in pod.subpods:
    #         print(sub.plaintext)
            # img_list.append(sub.img['@src'])
    return render_template('topics.html', name = name, topic=topic, skills=paginate.items, paginate=paginate, comments = comments)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return render_template('index.html')


@app.route('/test', methods=['GET','POST'])
def test():
    return render_template('test.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    from models import db
    email = session.get('EMAIL')
    student = Student.query.filter(Student.student_email == email).first()
    teacher = Teacher.query.filter(Teacher.teacher_email == email).first()
    if student:
        form = UpdateInfo()
    # if student.agent_photo != None:
    #     image = open(os.path.join(app.config['UPLOAD_PATH'], student.agent_photo), 'rb')
    #     img_stream = image.read()
    #     img_stream = base64.b64encode(img_stream).decode('ascii')
    # else:
        name = student.student_lastname
        image = open('static/images/icon/' + name[0] + ".png", 'rb')
        img_stream = image.read()
        img_stream = base64.b64encode(img_stream).decode('ascii')
        user_info = {
            'email': email,
            'first_name': student.student_firstname,
            'last_name': student.student_lastname,
            'profile_pic': img_stream,
            'phone': student.student_phone,
            'school': student.student_school,
            'address': student.student_address,
            'age': datetime.now().date().year - int(student.student_dob.split("-")[0]),
            'gender': student.student_gender,
            'password':student.student_password,
            'occupation': 'Student'
        }
        if form.validate_on_submit():
            student_in_db = Student.query.filter(Student.student_email == email).first()
            student_in_db.student_firstname = form.firstname.data
            student_in_db.student_lastname = form.lastname.data
            student_in_db.student_phone = form.phone.data
            student_in_db.student_address = form.address.data
            student_in_db.student_school = form.school.data
            db.session.add(student_in_db)
            db.session.commit()
            session.clear()
            flash('Information has been updated')
            return redirect(url_for('signin'))
    elif teacher:
        form = TeacherUpdateInfo()
        name = teacher.teacher_lastname
        image = open('static/images/icon/' + name[0] + ".png", 'rb')
        img_stream = image.read()
        img_stream = base64.b64encode(img_stream).decode('ascii')
        user_info = {
            'email': email,
            'first_name': teacher.teacher_firstname,
            'last_name': teacher.teacher_lastname,
            'profile_pic': img_stream,
            'phone': teacher.teacher_phone,
            'school': teacher.teacher_school,
            'password': teacher.teacher_password,
            'occupation': 'Teacher'
        }
        if form.validate_on_submit():
            teacher_in_db = Teacher.query.filter(Teacher.teacher_email == email).first()
            teacher_in_db.teacher_firstname = form.firstname.data
            teacher_in_db.teacher_lastname = form.lastname.data
            teacher_in_db.teacher_phone = form.phone.data
            teacher_in_db.teacher_school = form.school.data
            db.session.add(teacher_in_db)
            db.session.commit()
            session.clear()
            flash('Information has been updated')
            return redirect(url_for('signin'))
    return render_template('profile.html', user=user_info, form=form)


if __name__ == '__main__':
    app.run(debug = True)

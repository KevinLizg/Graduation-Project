import base64
import collections
import itertools
import os
import random, json
import urllib

import wolframalpha
import xmltodict
# from mathgenerator import mathgen
from mathgenerator import mathgen

from flask import Flask, render_template, url_for, jsonify, redirect, flash, session, request
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_mail import Message, Mail
from werkzeug.security import generate_password_hash, check_password_hash

from form import *

from config import Config
from flask_sqlalchemy import SQLAlchemy, Pagination
from models import *

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

################# Wolfram Query ###################
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
####################################################


################# Clear Cached ###################
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


# app name
@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
    name = session.get('NAME')
    email = session.get('EMAIL')
    session['NAME'] = name
    session['EMAIL'] = email
    return render_template("404.html")


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    email = session.get('EMAIL')
    name = session.get('NAME')
    session['NAME'] = name
    session['EMAIL'] = email
    student_in_db = Student.query.filter(Student.email == email).first()
    teacher_in_db = Teacher.query.filter(Teacher.email == email).first()
    user = ''
    if student_in_db:
        user = student_in_db
    if teacher_in_db:
        user = teacher_in_db
    return render_template('index.html', user=user)


app.config["MAIL_SERVER"] = 'smtp.qq.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = '1575631865@qq.com'
app.config['MAIL_PASSWORD'] = 'edhkaigxljyubaaa'
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
        user_in_db = Student.query.filter(Student.email == email).first()
        teacher_in_db = Teacher.query.filter(Teacher.email == email).first()
        if not user_in_db:
            if teacher_in_db:
                flash('This email has been signed up as a teacher account!')
            else:
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
    return render_template('email_verification.html', form=form)


@app.route('/teacher_email_verification', methods=['GET', 'POST'])
def teacher_email_verification():
    form = TeacherEmailVeriForm()
    if form.validate_on_submit() and form.token.data == 'TCSNUP':
        email = form.email.data
        user_in_db = Teacher.query.filter(Teacher.email == email).first()
        student_in_db = Student.query.filter(Student.email == email).first()
        if not user_in_db:
            if student_in_db:
                flash('This email has been signed up as a student account!')
            else:
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
    elif form.token.data != 'TCSNUP':
        flash('The token is not correct')
    return render_template('teacher_email_verification.html', form=form)


@app.route('/change_pass_verification', methods=['GET', 'POST'])
def change_pass_verification():
    form = EmailVeriForm()
    if form.validate_on_submit():
        email = form.email.data
        student_in_db = Student.query.filter(Student.email == email).first()
        teacher_in_db = Teacher.query.filter(Teacher.email == email).first()
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
    return render_template('change_pass_verification.html', form=form)


@app.route('/change_password/<token>', methods=['GET', 'POST'])
def change_password(token):
    from models import db
    form = ChangePassword()
    user_type = session.get('ACTOR')
    try:
        email = s.loads(token, salt='email-confirm', max_age=180)
        if form.validate_on_submit() and user_type == 'Student':
            student = Student.query.filter(Student.email == session.get('EMAIL')).first()
            student.student_password = generate_password_hash(form.password.data)
            db.session.add(student)
            db.session.commit()
            session.clear()
            flash("Change successfully")
            return redirect(url_for('signin'))
        elif form.validate_on_submit() and user_type == 'Teacher':
            teacher = Teacher.query.filter(Teacher.email == session.get('EMAIL')).first()
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
    teachers = Teacher.query.all()
    teacher_list = []
    for teacher in teachers:
        teacher_list.append((teacher.id, teacher.firstname+" "+teacher.lastname+" from "+teacher.school))
    form.teacher.choices = teacher_list
    try:
        email = s.loads(token, salt='email-confirm', max_age=180)
        if form.validate_on_submit():
            if form.firstname.data.isalpha() and form.lastname.data.isalpha():
                passw_hash = generate_password_hash(form.password.data)
                student = Student(email=email, teacher_id=form.teacher.data, firstname=form.firstname.data, lastname=form.lastname.data,
                                  password=passw_hash, gender=form.gender.data, phone=form.phone.data,
                                  school=form.school.data, dob=form.dob.data, address=form.address.data,
                                  profile_photo=form.lastname.data[0])
                db.session.add(student)
                db.session.commit()
                session.clear()
                flash('Sign up successfully')
                return redirect(url_for('signin'))
            else:
                flash('Your name could only contain letter of alphabet')
    except SignatureExpired:
        flash('Token is expired, please resend an email to sign up')
        return redirect(url_for('email_varification'))
    return render_template('signup.html', form=form)


@app.route('/signup_teacher/<token>', methods=['GET', 'POST'])
def signup_teacher(token):
    form = TeacherSignupForm()
    try:
        email = s.loads(token, salt='email-confirm', max_age=180)
        if form.validate_on_submit():
            if form.firstname.data.isalpha() and form.lastname.data.isalpha():
                passw_hash = generate_password_hash(form.password.data)
                teacher = Teacher(email=email, firstname=form.firstname.data, lastname=form.lastname.data,
                                  password=passw_hash, phone=form.phone.data,
                                  school=form.school.data, profile_photo=form.lastname.data[0])
                db.session.add(teacher)
                db.session.commit()
                session.clear()
                flash('Sign up successfully')
                return redirect(url_for('signin'))
            else:
                flash('Your name could only contain letter of alphabet')
    except SignatureExpired:
        flash('Token is expired, please resend an email to sign up')
        return redirect(url_for('teacher_email_verification'))
    return render_template('signup_teacher.html', form=form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        psw = form.password.data
        student_in_db = Student.query.filter(Student.email == form.email.data).first()
        teacher_in_db = Teacher.query.filter(Teacher.email == form.email.data).first()
        if student_in_db:
            if check_password_hash(student_in_db.password, psw):
                print('Login Success')
                session['NAME'] = student_in_db.firstname
                session['EMAIL'] = student_in_db.email
                session['ACTOR'] = 'Student'
                return redirect(url_for("index"))
            else:
                flash('Incorrect password')
                return redirect(url_for("signin"))
        elif teacher_in_db:
            if check_password_hash(teacher_in_db.password, psw):
                print('Login Success')
                session['NAME'] = teacher_in_db.firstname
                session['EMAIL'] = teacher_in_db.email
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
    email = session.get('EMAIL')
    student_in_db = Student.query.filter(Student.email == email).first()
    teacher_in_db = Teacher.query.filter(Teacher.email == email).first()
    user = ''
    if student_in_db:
        user = student_in_db
    if teacher_in_db:
        user = teacher_in_db
    topic_ = Topics.query.filter(Topics.topic_name == topic).first()
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 3))
    paginate = Skills.query.filter(Skills.topic_id == topic_.topic_id).paginate(page, per_page, error_out=False)
    info = []
    skills = paginate.items
    for skill in skills:
        info.append({
            'comment': Comments.query.filter(Comments.skill_id == skill.skill_id).count(),
            'image': skill.skill_name + '.png'
        })
    comment_info = []
    comment_detail = Comments.query.filter(Comments.topic_id == topic_.topic_id).order_by(
        Comments.comment_time.desc()).all()
    for comment in comment_detail[:3]:
        skill_name = Skills.query.filter(Skills.skill_id == comment.skill_id).first().skill_name
        comment_info.append({
            'comment': comment,
            'skill_name': skill_name
        })
    topic_info = []
    all_topic = Topics.query.all()
    for topic_ in all_topic:
        topic_info.append({
            'skill_count': Skills.query.filter(Skills.topic_id == topic_.topic_id).count(),
            'topic_name': topic_.topic_name
        })
    return render_template('topics.html', user=user, topic=topic, skills=paginate.items, paginate=paginate, info=info,
                           comment_info=comment_info, all_topic=topic_info)


@app.route('/skill_details/<skill_>', methods=['GET', 'POST'])
def skill_details(skill_):
    name = session.get('NAME')
    email = session.get('EMAIL')
    if (name):
        session['NAME'] = name
        session['EMAIL'] = email
        replyForm = ReplyForm()
        commentForm = CommentForm()
        skill = Skills.query.filter(Skills.skill_name == skill_).first()
        all_skill = [skill.skill_name for skill in Skills.query.filter(Skills.topic_id == skill.topic_id).all()]
        comments_in_db = Comments.query.filter(Comments.skill_id == skill.skill_id).order_by(
            Comments.comment_time.desc()).all()
        comments = []
        user_in_db = ''
        user_type = 1
        student_in_db = Student.query.filter(Student.email == email).first()
        teacher_in_db = Teacher.query.filter(Teacher.email == email).first()
        if student_in_db:
            user_in_db = student_in_db
        if teacher_in_db:
            user_in_db = teacher_in_db
            user_type = 0
        like = Like.query.filter(
            Like.user_type == user_type, Like.skill_id == skill.skill_id, Like.user_id == user_in_db.id).first()
        print(like)
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 3))
        paginate = Comments.query.filter(Comments.skill_id == skill.skill_id).order_by(
            Comments.comment_time.desc()).paginate(page, per_page, error_out=False)
        comment_count = Comments.query.filter(Comments.skill_id == skill.skill_id).count()
        for comment in paginate.items:
            user = ''
            if comment.user_type == 1:
                user = Student.query.filter(Student.id == comment.user_id).first()
            elif comment.user_type == 0:
                user = Teacher.query.filter(Teacher.id == comment.user_id).first()
            reply_list = []
            replies = Reply.query.filter(Reply.comment_id == comment.comment_id).all()
            for reply in replies:
                if reply.user_type == 1:
                    reply_user = Student.query.filter(Student.id == reply.user_id).first()
                elif reply.user_type == 0:
                    reply_user = Teacher.query.filter(Teacher.id == comment.user_id).first()
                image = open('static/images/icon/' + reply_user.profile_photo + ".png", 'rb')
                img_stream = image.read()
                img_stream = base64.b64encode(img_stream).decode('ascii')
                if reply_user.badge_name:
                    reply_badge = reply_user.badge_name.split('_')[1]
                    badge = base64.b64encode(
                        open('static/images/badge/' + reply_user.badge_name + ".png", 'rb').read()).decode('ascii')
                else:
                    reply_badge = None
                    badge = None
                reply_list.append({
                    'reply_content': reply.reply_content,
                    'reply_email': reply_user.email,
                    'reply_user_name': reply_user.firstname + ', ' + reply_user.lastname,
                    'reply_time': reply.reply_time,
                    'reply_img': img_stream,
                    'color': reply_badge,
                    'badge_name': badge
                })
            image = open('static/images/icon/' + user.profile_photo + ".png", 'rb')
            img_stream = image.read()
            img_stream = base64.b64encode(img_stream).decode('ascii')
            if user.badge_name:
                badge_name = user.badge_name.split('_')[1]
                badge = base64.b64encode(
                    open('static/images/badge/' + user.badge_name + ".png", 'rb').read()).decode('ascii')
            else:
                badge_name = None
                badge = None
            comments.append({
                'comment_id': comment.comment_id,
                'comment': comment.comment,
                'user_name': user.firstname + ', ' + user.lastname,
                'user_email': user.email,
                'comment_time': comment.comment_time,
                'replies': reply_list,
                'user_img': img_stream,
                'color': badge_name,
                'badge_name': badge
            })
        if replyForm.validate_on_submit():
            reply_add = Reply(reply_content=replyForm.reply.data, comment_id=replyForm.comment_id.data,
                              user_id=user_in_db.id,
                              user_type=user_type,
                              reply_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            db.session.add(reply_add)
            db.session.commit()
            session['NAME'] = name
            session['EMAIL'] = email
            return redirect(url_for('skill_details', skill_=skill_))
        if commentForm.validate_on_submit():
            topic_id = Skills.query.filter(Skills.skill_id == skill.skill_id).first().topic_id
            comment_add = Comments(comment=commentForm.comment.data, skill_id=skill.skill_id,
                                   user_id=user_in_db.id, user_type=user_type, topic_id=topic_id,
                                   comment_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            db.session.add(comment_add)
            db.session.commit()
            session.clear()
            session['NAME'] = name
            session['EMAIL'] = email
            return redirect(url_for('skill_details', skill_=skill_))
    else:
        flash("Please sign in first")
        return redirect(url_for('signin'))
    return render_template('skill_details.html', skill=skill, comments=comments, replyForm=replyForm,
                           commentForm=commentForm, user_type=user_type,
                           user=user_in_db, all_skill=all_skill,
                           paginate=paginate, comment_count=comment_count, like=like
                           )


@app.route('/shop', methods=['GET', 'POST'])
def shop():
    name = session.get('NAME')
    email = session.get('EMAIL')
    user_avatar = []
    if (name):
        session['NAME'] = name
        session['EMAIL'] = email
        avatar_list = []
        badge_list = []
        student_in_db = Student.query.filter(Student.email == email).first()
        teacher_in_db = Teacher.query.filter(Teacher.email == email).first()
        user = ''
        user_type = 1
        if student_in_db:
            user = student_in_db
        elif teacher_in_db:
            user = teacher_in_db
            user_type = 0
        time_capsule_list = [{
            'name': 'Time Capsule Type 1',
            'price': 80,
            'description': 'This could help you add more time in the quiz so that you could finish your quiz, this capsule will add 10 seconds for you',
            'image': 'capsule1',
            'type': 1
        }, {
            'name': 'Time_Capsule_Type_2',
            'price': 120,
            'description': 'This could help you add more time in the quiz so that you could finish your quiz, this capsule will add 20 seconds for you',
            'image': 'capsule2',
            'type': 2
        }]
        for avatar_file in os.listdir('static/images/avatar'):
            avatar = Avatar.query.filter(Avatar.user_id == user.id, Avatar.user_type == user_type,
                                         Avatar.avatar_name == avatar_file.split('.')[0]).first()
            avatar_have = False
            if avatar:
                avatar_have = True
            avatar_list.append({
                'have': avatar_have,
                'name': avatar_file.split('.')[0],
                'price': 100,
                'image': base64.b64encode(open('static/images/avatar/' + avatar_file, 'rb').read()).decode('ascii')
            })
        for badge_file in os.listdir('static/images/badge'):
            badge = Badge.query.filter(Badge.user_id == user.id, Badge.user_type == user_type,
                                       Badge.badge_name == badge_file.split('.')[0]).first()
            badge_have = False
            if badge:
                badge_have = True
            badge_list.append({
                'have': badge_have,
                'name': badge_file.split('.')[0],
                'price': 50,
                'image': base64.b64encode(open('static/images/badge/' + badge_file, 'rb').read()).decode('ascii')
            })
    else:
        flash("Please sign in first")
        return redirect(url_for('signin'))
    return render_template('shop.html', avatar_list=avatar_list, time_capsule_list=time_capsule_list,
                           user=user, coins=user.coins, badge_list=badge_list)


@app.route('/shop_buy/<price>', methods=['GET', 'POST'])
def shop_buy(price):
    from models import db
    email = session.get('EMAIL')
    student = Student.query.filter(Student.email == email).first()
    teacher = Teacher.query.filter(Teacher.email == email).first()
    name = request.form.get("name")
    type = request.form.get("type")
    user = ''
    user_type = 1
    if student:
        user = student
    if teacher:
        user = teacher
        user_type = 0
    if type == 'avatar':
        avatar = Avatar(user_id=user.id, avatar_name=name, user_type=user_type)
        if user.coins >= int(price):
            user.coins -= int(price)
            db.session.add(user)
            db.session.add(avatar)
            db.session.commit()
    if type == 'badge':
        badge = Badge(user_id=user.id, badge_name=name, user_type=user_type)
        if user.coins >= int(price):
            user.coins -= int(price)
            db.session.add(user)
            db.session.add(badge)
            db.session.commit()
    num = request.form.get("num")
    if type == 'capsule':
        if name == '1':
            user.time_capsule1 += int(num)
        if name == '2':
            user.time_capsule2 += int(num)
        if user.coins >= int(price):
            user.coins -= int(price)
            db.session.add(user)
            db.session.commit()
    return 'hello'


@app.route('/ready/<skill_>', methods=["GET", "POST"])
def ready(skill_):
    name = session.get('NAME')
    email = session.get('EMAIL')
    if (name):
        session['NAME'] = name
        session['EMAIL'] = email
        student_in_db = Student.query.filter(Student.email == email).first()
        teacher_in_db = Teacher.query.filter(Teacher.email == email).first()
        user = ''
        if student_in_db:
            user = student_in_db
        if teacher_in_db:
            user = teacher_in_db
    else:
        flash("Please sign in first")
        return redirect(url_for('signin'))
    return render_template("ready.html", filename=email + ".json", user=user, skill_=skill_)


skill_dict = {
            # Good
            1: [0, 1],
            # Good
            2: [2, 3],
            # Good
            3: [6, 8],
            # Good
            4: [13, 16, 28],
            # Good
            5: [53],
            # Good
            6: [11],
            # Good
            7: [21],
            # Good
            8: [111],
            # Good
            9: [24],
            # Good
            10: [50],
            # Good
            11: [26],
            # Good
            12: [18, 19, 22, 25],
            # Good
            13: [32, 33, 34, 38],
            # Good
            14: [35, 36, 37, 39],
            # Good
            15: [112, 75, 115],
            # Good
            16: [114],
            # Not good
            17: [30, 42],
            # Good
            18: [59,124,125],
            # Good
            19: [40, 10],
            # Good
            20: [101, 102],
            # Good
            21: [27],
            22: [55],
}
@app.route('/practice/<skill_>')
def practice(skill_):
    name = session.get('NAME')
    email = session.get('EMAIL')
    if (name):
        session['NAME'] = name
        session['EMAIL'] = email
        student_in_db = Student.query.filter(Student.email == email).first()
        teacher_in_db = Teacher.query.filter(Teacher.email == email).first()
        user = ''
        if student_in_db:
            user = student_in_db
        if teacher_in_db:
            user = teacher_in_db
        skill = Skills.query.filter(Skills.skill_name == skill_).first()
        list = []
        for i in range(0, 5):
            ran_num = random.randint(0, len(skill_dict[skill.skill_id]) - 1)
            problem, solution = mathgen.genById(skill_dict[skill.skill_id][ran_num])
            app_id = 'XQAUEU-WR3AY23332'
            client = wolframalpha.Client(app_id)
            # res = client.query(problem)
            res = query(problem, app_id)
            img_list = []
            solution_list = []
            for pod in res.pods:
                for sub in pod.subpods:
                    img_list.append(sub.img['@src'])
                    solution_list.append(sub.plaintext)
            option_list = [solution]
            if skill_dict[skill.skill_id][ran_num] == 19:
                if solution == 'Exist':
                    option_list.append('Do not exist')
                else:
                    option_list.append('Exist')
            if skill_dict[skill.skill_id][ran_num] == 101:
                if solution == 'is a leap year':
                    option_list.append('is not a leap year')
                else:
                    option_list.append('is a leap year')
            if skill_dict[skill.skill_id][ran_num] == 55:
                if solution == '>':
                    option_list.append('<')
                    option_list.append('=')
                elif solution == '=':
                    option_list.append('<')
                    option_list.append('>')
                else:
                    option_list.append('>')
                    option_list.append('=')
            if skill_dict[skill.skill_id][ran_num] != 19 and skill_dict[skill.skill_id][ran_num] != 101 and skill_dict[skill.skill_id][ran_num] != 55:
                for j in range(1, 4):
                    gen_problem, gen_solution = mathgen.genById(skill_dict[skill.skill_id][ran_num])
                    option_list.append(gen_solution)
                while len(set(option_list)) != len(option_list):
                    op_dict = dict(Counter(option_list))
                    for key, value in op_dict.items():
                        if value > 1:
                            option_list.remove(key)
                            gen_problem, gen_solution = mathgen.genById(skill_dict[skill.skill_id][ran_num])
                            option_list.append(gen_solution)
            random.shuffle(option_list)
            if skill_dict[skill.skill_id][ran_num] == 19:
                answer = ["A", "B"]
            if skill_dict[skill.skill_id][ran_num] == 55:
                answer = ["A", "B", "C"]
            if skill_dict[skill.skill_id][ran_num] != 55 and skill_dict[skill.skill_id][ran_num] != 19:
                answer = ["A", "B", "C", "D"]
            idx = 0
            if skill.skill_id == 10:
                problem = 'Zero Interval of: ' + problem
            for op in option_list:
                if op == solution:
                    an = answer[idx]
                idx += 1
            list.append({
                'id': i,
                'title': problem,
                'option': option_list,
                'answer': an,
                'analysis': img_list,
                'skill': skill.skill_name
            })
        with open('static/json/' + email + '.json', 'w', encoding='utf-8') as f:
            json.dump(list, f, ensure_ascii=False, indent=4)
    else:
        flash("Please sign in first")
        return redirect(url_for('signin'))
    return render_template('practice.html', user=user, coins=user.coins, skill_=skill_)


from os.path import exists


@app.route('/wrong_problem_add/<question_id>', methods=["GET", "POST"])
def wrong_problem_add(question_id):
    email = request.form.get("email")
    check = request.form.get("check")
    print(check)
    with open('static/json/' + email + '.json', 'r', encoding='utf-8') as f:
        question_list = json.load(f)
    for question in question_list:
        if question['id'] == int(question_id):
            if exists('static/json/wrong/' + email+'.json'):
                with open('static/json/wrong/' + email + '.json', 'r', encoding='utf-8') as f:
                    wrong_question_list = json.load(f)
                    new_id = len(wrong_question_list)
                    wrong_question_list.append({
                        'id': new_id,
                        'title': question['title'],
                        'option': question['option'],
                        'answer': question['answer'],
                        'skill': question['skill'],
                        'check': check
                    })
                    f.close()
            else:
                wrong_question_list = []
                wrong_question_list.append({
                    'id': 0,
                    'title': '',
                    'option': '',
                    'answer': '',
                    'skill': '',
                })
                with open('static/json/wrong/' + email + '.json', 'w', encoding='utf-8') as f:
                    json.dump(wrong_question_list, f, ensure_ascii=False, indent=4)
                    f.close()
                for question in question_list:
                    if question['id'] == int(question_id):
                        with open('static/json/wrong/' + email + '.json', 'r', encoding='utf-8') as f:
                            wrong_question_list = json.load(f)
                            new_id = len(wrong_question_list)
                            wrong_question_list.append({
                                'id': new_id,
                                'title': question['title'],
                                'option': question['option'],
                                'answer': question['answer'],
                                'skill': question['skill'],
                                'check': check
                            })
                            f.close()
    with open('static/json/wrong/' + email + '.json', 'w', encoding='utf-8') as f:
        json.dump(wrong_question_list, f, ensure_ascii=False, indent=4)
        f.close()
    return 'wrong_problem_add'


@app.route('/wrong_problem_update/<question_id>', methods=["GET", "POST"])
def wrong_problem_update(question_id):
    email = request.form.get("email")
    check = request.form.get("check")
    with open('static/json/wrong/' + email + '.json', 'r', encoding='utf-8') as f:
        wrong_question_list = json.load(f)
    for wrong_question in wrong_question_list:
        if wrong_question['id'] == int(question_id):
            wrong_question['check'] = check
    with open('static/json/wrong/' + email + '.json', 'w', encoding='utf-8') as f:
        json.dump(wrong_question_list, f, ensure_ascii=False, indent=4)
        f.close()
    return 'wrong_problem_update'


@app.route('/wrong_problem_delete/<question_id>', methods=["GET", "POST"])
def wrong_problem_delete(question_id):
    email = request.form.get("email")
    with open('static/json/wrong/' + email + '.json', 'r', encoding='utf-8') as f:
        wrong_question_list = json.load(f)
    for wrong_question in wrong_question_list:
        if wrong_question['id'] == int(question_id):
            del wrong_question_list[int(question_id)]
    for idx in range(1,len(wrong_question_list)):
        wrong_question_list[idx]['id'] = idx
    with open('static/json/wrong/' + email + '.json', 'w', encoding='utf-8') as f:
        json.dump(wrong_question_list, f, ensure_ascii=False, indent=4)
        f.close()
    return 'wrong_problem_update'


@app.route('/wrong_collection', methods=["GET", "POST"])
def wrong_collection():
    name = session.get('NAME')
    email = session.get('EMAIL')
    if (name):
        session['NAME'] = name
        session['EMAIL'] = email
        student_in_db = Student.query.filter(Student.email == email).first()
        teacher_in_db = Teacher.query.filter(Teacher.email == email).first()
        user = ''
        if student_in_db:
            user = student_in_db
        if teacher_in_db:
            user = teacher_in_db
    filename = email+'.json'
    if not exists('static/json/wrong/' + filename):
        filename = None
        question_list = None
    else:
        with open('static/json/wrong/' + filename, 'r', encoding='utf-8') as f:
            question_list = json.load(f)
        for question in question_list[1:]:
            app_id = 'XQAUEU-WR3AY23332'
            res = query(question['title'], app_id)
            img_list = []
            for pod in res.pods:
                for sub in pod.subpods:
                    img_list.append(sub.img['@src'])
            question['analysis'] = img_list
        with open('static/json/wrong/' + email + '.json', 'w', encoding='utf-8') as f:
            json.dump(question_list, f, ensure_ascii=False, indent=4)
            f.close()
    return render_template('wrong_collection.html', user=user, filename=filename, question_list=question_list)


def query(input, app_id, params=(), **kwargs):
    data = dict(
        input=input,
        appid=app_id,
    )
    data = itertools.chain(params, data.items(), kwargs.items())
    query = urllib.parse.urlencode(tuple(data))
    url = 'https://api.wolframalpha.com/v2/query?' + query + '&podstate=Step-by-step%20solution'
    resp = urllib.request.urlopen(url)
    assert resp.headers.get_content_type() == 'text/xml'
    assert resp.headers.get_param('charset') == 'utf-8'
    doc = xmltodict.parse(resp, postprocessor=wolframalpha.Document.make)
    return doc['queryresult']


from collections import Counter
@app.route('/quiz/<skill_>')
def quiz(skill_):
    name = session.get('NAME')
    email = session.get('EMAIL')
    ###########################
    ### 重复答案的问题需要解决 ###
    ##########################
    if (name):
        session['NAME'] = name
        session['EMAIL'] = email
        student = Student.query.filter(Student.email == email).first()
        teacher = Teacher.query.filter(Teacher.email == email).first()
        if student:
            user = student
        if teacher:
            user = teacher
        skill = Skills.query.filter(Skills.skill_name == skill_).first()
        list = []
        for i in range(0, 10):
            ran_num = random.randint(0, len(skill_dict[skill.skill_id]) - 1)
            problem, solution = mathgen.genById(skill_dict[skill.skill_id][ran_num])
            app_id = 'XQAUEU-WR3AY23332'
            client = wolframalpha.Client(app_id)
            # res = client.query(problem)
            res = query(problem, app_id)
            img_list = []
            solution_list = []
            for pod in res.pods:
                for sub in pod.subpods:
                    img_list.append(sub.img['@src'])
                    solution_list.append(sub.plaintext)
            option_list = [solution]
            if skill_dict[skill.skill_id][ran_num] == 19:
                if solution == 'Exist':
                    option_list.append('Do not exist')
                else:
                    option_list.append('Exist')
            if skill_dict[skill.skill_id][ran_num] == 101:
                if solution == 'is a leap year':
                    option_list.append('is not a leap year')
                else:
                    option_list.append('is a leap year')
            if skill_dict[skill.skill_id][ran_num] == 55:
                if solution == '>':
                    option_list.append('<')
                    option_list.append('=')
                elif solution == '=':
                    option_list.append('<')
                    option_list.append('>')
                else:
                    option_list.append('>')
                    option_list.append('=')
            if skill_dict[skill.skill_id][ran_num] != 19 and skill_dict[skill.skill_id][ran_num] != 101 and skill_dict[skill.skill_id][ran_num] != 55:
                for j in range(1, 4):
                    gen_problem, gen_solution = mathgen.genById(skill_dict[skill.skill_id][ran_num])
                    option_list.append(gen_solution)
                while len(set(option_list)) != len(option_list):
                    op_dict = dict(Counter(option_list))
                    for key, value in op_dict.items():
                        if value > 1:
                            option_list.remove(key)
                            gen_problem, gen_solution = mathgen.genById(skill_dict[skill.skill_id][ran_num])
                            option_list.append(gen_solution)
            random.shuffle(option_list)
            if skill_dict[skill.skill_id][ran_num] == 55:
                answer = ["A", "B", "C"]
            if skill_dict[skill.skill_id][ran_num] == 19:
                answer = ["A", "B"]
            if skill_dict[skill.skill_id][ran_num] != 55 and skill_dict[skill.skill_id][ran_num] != 19:
                answer = ["A", "B", "C", "D"]
            idx = 0
            if skill.skill_id == 10:
                problem = 'Zero Interval of: '+problem
            for op in option_list:
                if op == solution:
                    an = answer[idx]
                idx += 1
            list.append({
                'id': i,
                'title': problem,
                'option': option_list,
                'answer': an,
                'analysis': img_list
            })
        with open('static/json/' + email + '.json', 'w', encoding='utf-8') as f:
            json.dump(list, f, ensure_ascii=False, indent=4)
    else:
        flash("Please sign in first")
        return redirect(url_for('signin'))
    return render_template('quiz.html', num=1 * 120, user=user, coins=user.coins, skill_=skill_,
                           timeCap1=user.time_capsule1, timeCap2=user.time_capsule2)


from collections import Counter
@app.route('/unit_test_main/')
def unit_test_main():
    topics = Topics.query.filter().all()
    name = session.get('NAME')
    email = session.get('EMAIL')
    ###########################
    ### 重复答案的问题需要解决 ###
    ##########################
    if (name):
        session['NAME'] = name
        session['EMAIL'] = email
        student = Student.query.filter(Student.email == email).first()
        teacher = Teacher.query.filter(Teacher.email == email).first()
        if student:
            user = student
        if teacher:
            user = teacher
    else:
        flash("Please sign in first")
        return redirect(url_for('signin'))
    return render_template('unit_test_main.html', user=user, topics=topics)


@app.route('/unit_test/<topic>')
def unit_test(topic):
    name = session.get('NAME')
    email = session.get('EMAIL')
    ###########################
    ### 重复答案的问题需要解决 ###
    ##########################
    if (name):
        session['NAME'] = name
        session['EMAIL'] = email
        student = Student.query.filter(Student.email == email).first()
        teacher = Teacher.query.filter(Teacher.email == email).first()
        if student:
            user = student
        if teacher:
            user = teacher
        topic = Topics.query.filter(Topics.topic_name == topic).first()
        skills = Skills.query.filter(Skills.topic_id == topic.topic_id).all()
        skill_id = []
        for skill in skills:
            skill_id.append(skill.skill_id)
        list = []
        for i in range(0, 20):
            skill_ran_num = skill_id[random.randint(0, len(skill_id)-1)]
            ran_num = random.randint(0, len(skill_dict[skill_ran_num]) - 1)
            problem, solution = mathgen.genById(skill_dict[skill_ran_num][ran_num])
            app_id = 'XQAUEU-WR3AY23332'
            client = wolframalpha.Client(app_id)
            # res = client.query(problem)
            res = query(problem, app_id)
            img_list = []
            solution_list = []
            for pod in res.pods:
                for sub in pod.subpods:
                    img_list.append(sub.img['@src'])
                    solution_list.append(sub.plaintext)
            option_list = [solution]
            if skill_dict[skill_ran_num][ran_num] == 19:
                for j in range(1, 2):
                    if solution == 'Exist':
                        option_list.append('Do not exist')
                    else:
                        option_list.append('Exist')
            if skill_dict[skill_ran_num][ran_num] == 101:
                if solution == 'is a leap year':
                    option_list.append('is not a leap year')
                else:
                    option_list.append('is a leap year')
            if skill_dict[skill_ran_num][ran_num] == 55:
                if solution == '>':
                    option_list.append('<')
                    option_list.append('=')
                elif solution == '=':
                    option_list.append('<')
                    option_list.append('>')
                else:
                    option_list.append('>')
                    option_list.append('=')
            if skill_dict[skill_ran_num][ran_num] != 19 and skill_dict[skill_ran_num][ran_num] != 101 and skill_dict[skill_ran_num][ran_num] != 55:
                for j in range(1, 4):
                    gen_problem, gen_solution = mathgen.genById(skill_dict[skill_ran_num][ran_num])
                    option_list.append(gen_solution)
                while len(set(option_list)) != len(option_list):
                    op_dict = dict(Counter(option_list))
                    for key, value in op_dict.items():
                        if value > 1:
                            option_list.remove(key)
                            gen_problem, gen_solution = mathgen.genById(skill_dict[skill_ran_num][ran_num])
                            option_list.append(gen_solution)
            random.shuffle(option_list)
            if skill_dict[skill_ran_num][ran_num] == 55:
                answer = ["A", "B", "C"]
            if skill_dict[skill_ran_num][ran_num] == 19:
                answer = ["A", "B"]
            if skill_dict[skill_ran_num][ran_num] != 55 and skill_dict[skill_ran_num][ran_num] != 19:
                answer = ["A", "B", "C", "D"]
            idx = 0
            if skill_ran_num == 10:
                problem = 'Zero Interval of: ' + problem
            for op in option_list:
                if op == solution:
                    an = answer[idx]
                idx += 1
            list.append({
                'id': i,
                'title': problem,
                'option': option_list,
                'answer': an,
                'analysis': img_list
            })
        with open('static/json/' + email + '.json', 'w', encoding='utf-8') as f:
            json.dump(list, f, ensure_ascii=False, indent=4)
    else:
        flash("Please sign in first")
        return redirect(url_for('signin'))
    return render_template('unit_test.html', num=1 * 120, user=user, coins=user.coins,
                           timeCap1=user.time_capsule1, timeCap2=user.time_capsule2, topic=topic)


@app.route('/return_time_capsule', methods=['GET', 'POST'])
def return_time_capsule():
    from models import db
    email = session.get('EMAIL')
    student = Student.query.filter(Student.email == email).first()
    teacher = Teacher.query.filter(Teacher.email == email).first()
    capsule1 = request.form.get("timeCap1")
    capsule2 = request.form.get("timeCap2")
    if student:
        user = student
    if teacher:
        user = teacher
    user.time_capsule1 = capsule1
    user.time_capsule2 = capsule2
    db.session.add(user)
    db.session.commit()
    return ''


@app.route('/return_like', methods=['GET', 'POST'])
def return_like():
    from models import db
    email = session.get('EMAIL')
    student = Student.query.filter(Student.email == email).first()
    teacher = Teacher.query.filter(Teacher.email == email).first()
    skill_name = request.form.get("skill_name")
    skill = Skills.query.filter(Skills.skill_name == skill_name).first()
    user = ''
    user_type = 1
    if student:
        user = student
    if teacher:
        user = teacher
        user_type = 0
    like = Like.query.filter(Like.user_type == user_type, Like.skill_id == skill.skill_id,
                             Like.user_id == user.id).first()
    if like:
        skill.like -= 1
        db.session.add(skill)
        db.session.delete(like)
        db.session.commit()
    else:
        skill.like += 1
        db.session.add(skill)
        new_like = Like(skill_id=skill.skill_id, user_id=user.id, user_type=user_type)
        db.session.add(new_like)
        db.session.commit()
    return ''


@app.route('/return_coins', methods=['GET', 'POST'])
def return_coins():
    name = session.get('NAME')
    email = session.get('EMAIL')
    if (name):
        session['NAME'] = name
        session['EMAIL'] = email
        from models import db
        student = Student.query.filter(Student.email == email).first()
        if student:
            coins = request.form.get("coins")
            student.coins = int(coins)
            db.session.add(student)
            db.session.commit()
        else:
            print('This is a teacher')
    else:
        flash("Please sign in first")
        return redirect(url_for('signin'))
    return 'coins'


@app.route('/return_result', methods=['GET', 'POST'])
def return_result():
    name = session.get('NAME')
    email = session.get('EMAIL')
    if (name):
        session['NAME'] = name
        session['EMAIL'] = email
        from models import db
        coins = request.form.get("coins")
        email = request.form.get("email")
        skill = request.form.get("skill")
        score = request.form.get("score")
        time = request.form.get("time")
        student = Student.query.filter(Student.email == email).first()
        teacher = Teacher.query.filter(Teacher.email == email).first()
        if student:
            skill = Skills.query.filter(Skills.skill_name == skill).first()
            score_add = Score(student_id=student.id, skill_id=skill.skill_id, score=score, time=time)
            db.session.add(score_add)
            db.session.commit()
            student.coins = int(coins)
            db.session.add(student)
            db.session.commit()
        if teacher:
            print('This is a teacher')
    else:
        flash("Please sign in first")
        return redirect(url_for('signin'))
    return 'result'


@app.route('/return_unit_result', methods=['GET', 'POST'])
def return_unit_result():
    name = session.get('NAME')
    email = session.get('EMAIL')
    if (name):
        session['NAME'] = name
        session['EMAIL'] = email
        from models import db
        coins = request.form.get("coins")
        email = request.form.get("email")
        topic_name = request.form.get("topic")
        score = request.form.get("score")
        time = request.form.get("time")
        student = Student.query.filter(Student.email == email).first()
        teacher = Teacher.query.filter(Teacher.email == email).first()
        if student:
            topic = Topics.query.filter(Topics.topic_name == topic_name).first()
            unit_add = Unit(student_id=student.id, topic_id=topic.topic_id, score=score, time=time)
            db.session.add(unit_add)
            db.session.commit()
            student.coins = int(coins)
            db.session.add(student)
            db.session.commit()
        if teacher:
            print('This is a teacher')
    else:
        flash("Please sign in first")
        return redirect(url_for('signin'))
    return 'result'


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return render_template('index.html')


@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('test.html')


@app.route('/user_profile/<user_email>', methods=['GET', 'POST'])
def user_profile(user_email):
    name = session.get('NAME')
    email = session.get('EMAIL')
    if name:
        session['NAME'] = name
        session['EMAIL'] = email
        user_email = user_email
        m_student = Student.query.filter(Student.email == user_email).first()
        m_teacher = Teacher.query.filter(Teacher.email == user_email).first()
        me_student = Student.query.filter(Student.email == email).first()
        me_teacher = Teacher.query.filter(Teacher.email == email).first()
        me = ''
        if me_student:
            me = me_student
            occupation = 'Student'
        if me_teacher:
            me = me_teacher
            occupation = 'Teacher'
        me_i = open('static/images/icon/' + me.profile_photo + ".png", 'rb')
        me_img = me_i.read()
        me_img = base64.b64encode(me_img).decode('ascii')
        if me.badge_name:
            color = me.badge_name.split('_')[1]
            badge = base64.b64encode(open('static/images/badge/' + me.badge_name + ".png", 'rb').read()).decode(
                'ascii')
        else:
            color = None
            badge = None
        my_info = {
            'email': email,
            'first_name': me.firstname,
            'last_name': me.lastname,
            'color': color,
            'badge_name': badge,
            'profile_pic': me_img,
            'occupation': occupation
        }
        if m_student:
            student = Student.query.filter(Student.email == user_email).first()
            scores = Score.query.filter(Score.student_id == student.id).order_by(Score.date.desc()).all()
            skill_name_dict = {}
            topic_master_dict = {}
            topic_master_count = {}
            score_list = []
            for score in scores:
                skill = Skills.query.filter(Skills.skill_id == score.skill_id).first()
                topic = Topics.query.filter(Topics.topic_id == skill.topic_id).first()
                comment = Comments.query.filter(Comments.skill_id == skill.skill_id).count()
                t_name = topic.topic_name
                s_name = skill.skill_name
                score_list.append({
                    'score': score.score,
                    'date': score.date,
                    'topics': t_name,
                    'skill': s_name,
                    'comment': comment,
                    'like': skill.like
                })
                if skill_name_dict.get(s_name) is None:
                    skill_name_dict[s_name] = 1
                else:
                    skill_name_dict[s_name] += 1
                if topic_master_count.get(t_name) is None:
                    topic_master_count[t_name] = 1
                else:
                    topic_master_count[t_name] += 1
                if topic_master_dict.get(t_name) is None:
                    topic_master_dict[t_name] = int(score.score)
                else:
                    topic_master_dict[t_name] += int(score.score)
            for k in topic_master_dict.keys():
                topic_master_dict[k] = int(topic_master_dict[k] / topic_master_count[k])
            skill_statistic = {
                'skill_list': list(skill_name_dict.keys()),
                'skill_value_list': list(skill_name_dict.values()),
            }
            image = open('static/images/icon/' + student.profile_photo + ".png", 'rb')
            img_stream = image.read()
            img_stream = base64.b64encode(img_stream).decode('ascii')
            if student.badge_name:
                color = student.badge_name.split('_')[1]
                badge = base64.b64encode(open('static/images/badge/' + student.badge_name + ".png", 'rb').read()).decode(
                    'ascii')
            else:
                color = None
                badge = None
            score_list, skill_statistic, topic_master_dict = return_score(student)
            user_info = {
                'email': user_email,
                'coins': student.coins,
                'first_name': student.firstname,
                'last_name': student.lastname,
                'profile_pic': img_stream,
                'phone': student.phone,
                'school': student.school,
                'address': student.address,
                'age': datetime.now().date().year - int(student.dob.split("-")[0]),
                'gender': student.gender,
                'password': student.password,
                'color': color,
                'badge_name': badge,
                'occupation': 'Student'
            }
        elif m_teacher:
            teacher = Teacher.query.filter(Teacher.email == user_email).first()
            skill_statistic = {}
            topic_master_dict = {}
            score_list = []
            form = TeacherUpdateInfo()
            name = teacher.lastname
            image = open('static/images/icon/' + teacher.profile_photo + ".png", 'rb')
            img_stream = image.read()
            img_stream = base64.b64encode(img_stream).decode('ascii')
            if teacher.badge_name:
                color = teacher.badge_name.split('_')[1]
                badge = base64.b64encode(open('static/images/badge/' + teacher.badge_name + ".png", 'rb').read()).decode(
                    'ascii')
            else:
                color = None
                badge = None
            user_info = {
                'email': user_email,
                'coins': teacher.coins,
                'first_name': teacher.firstname,
                'last_name': teacher.lastname,
                'profile_pic': img_stream,
                'phone': teacher.phone,
                'school': teacher.school,
                'password': teacher.password,
                'color': color,
                'badge_name': badge,
                'occupation': 'Teacher'
            }
    else:
        flash("Please sign in first")
        return redirect(url_for('signin'))
    return render_template('user_profile.html', name=name, email=email, user_info=user_info,
                           skill_list=json.dumps(skill_statistic),
                           topic_master=topic_master_dict, score_list=score_list, user=my_info, unit_score=None)


def return_score(student):
    scores = Score.query.filter(Score.student_id == student.id).order_by(Score.date.desc()).all()
    skill_name_dict = {}
    topic_master_dict = {}
    topic_master_count = {}
    score_list = []
    for score in scores:
        skill = Skills.query.filter(Skills.skill_id == score.skill_id).first()
        topic = Topics.query.filter(Topics.topic_id == skill.topic_id).first()
        comment = Comments.query.filter(Comments.skill_id == skill.skill_id).count()
        t_name = topic.topic_name
        s_name = skill.skill_name
        score_list.append({
            'score': score.score,
            'date': score.date,
            'topics': t_name,
            'skill': s_name,
            'comment': comment,
            'like': skill.like
        })
        if skill_name_dict.get(s_name) is None:
            skill_name_dict[s_name] = 1
        else:
            skill_name_dict[s_name] += 1
        if topic_master_count.get(t_name) is None:
            topic_master_count[t_name] = 1
        else:
            topic_master_count[t_name] += 1
        if topic_master_dict.get(t_name) is None:
            topic_master_dict[t_name] = int(score.score)
        else:
            topic_master_dict[t_name] += int(score.score)
    for k in topic_master_dict.keys():
        topic_master_dict[k] = int(topic_master_dict[k] / topic_master_count[k])
    skill_statistic = {
        'skill_list': list(skill_name_dict.keys()),
        'skill_value_list': list(skill_name_dict.values()),
    }
    return score_list, skill_statistic, topic_master_dict


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    from models import db
    email = session.get('EMAIL')
    print(email)
    if email:
        student = Student.query.filter(Student.email == email).first()
        teacher = Teacher.query.filter(Teacher.email == email).first()
        if student:
            subscribers = Follow.query.filter(Follow.user_id == student.id, Follow.user_type == 1).count()
            following = Follow.query.filter(Follow.follower_id == student.id, Follow.follower_type == 1).count()
            score_list, skill_statistic, topic_master_dict = return_score(student)
            form = UpdateInfo()
            image = open('static/images/icon/' + student.profile_photo + ".png", 'rb')
            img_stream = image.read()
            img_stream = base64.b64encode(img_stream).decode('ascii')
            if student.badge_name:
                color = student.badge_name.split('_')[1]
                badge = base64.b64encode(open('static/images/badge/' + student.badge_name + ".png", 'rb').read()).decode(
                    'ascii')
            else:
                color = None
                badge = None
            user_info = {
                'email': email,
                'first_name': student.firstname,
                'last_name': student.lastname,
                'profile_pic': img_stream,
                'phone': student.phone,
                'school': student.school,
                'address': student.address,
                'age': datetime.now().date().year - int(student.dob.split("-")[0]),
                'gender': student.gender,
                'password': student.password,
                'color': color,
                'badge_name': badge,
                'occupation': 'Student'
            }
            likes = Like.query.filter(Like.user_id == student.id, Like.user_type == 1).all()
            like_list = []
            for like in likes:
                skill = Skills.query.filter(Skills.skill_id == like.skill_id).first()
                like_list.append({
                    'skill_name': skill.skill_name,
                    'like_num': skill.like
                })
            if form.validate_on_submit():
                student_in_db = Student.query.filter(Student.email == email).first()
                student_in_db.firstname = form.firstname.data
                student_in_db.lastname = form.lastname.data
                student_in_db.phone = form.phone.data
                student_in_db.address = form.address.data
                student_in_db.school = form.school.data
                db.session.add(student_in_db)
                db.session.commit()
                session.clear()
                flash('Information has been updated')
                return redirect(url_for('signin'))
        elif teacher:
            students = Student.query.filter(Student.teacher_id == teacher.id).all()
            subscribers = Follow.query.filter(Follow.user_id == teacher.id, Follow.user_type == 0).count()
            following = Follow.query.filter(Follow.follower_id == teacher.id, Follow.follower_type == 0).count()
            skill_statistic = {}
            topic_master_dict = {}
            score_list = []
            form = TeacherUpdateInfo()
            image = open('static/images/icon/' + teacher.profile_photo + ".png", 'rb')
            img_stream = image.read()
            img_stream = base64.b64encode(img_stream).decode('ascii')
            if teacher.badge_name:
                color = teacher.badge_name.split('_')[1]
                badge = base64.b64encode(open('static/images/badge/' + teacher.badge_name + ".png", 'rb').read()).decode(
                    'ascii')
            else:
                color = None
                badge = None
            user_info = {
                'email': email,
                'first_name': teacher.firstname,
                'last_name': teacher.lastname,
                'profile_pic': img_stream,
                'phone': teacher.phone,
                'school': teacher.school,
                'password': teacher.password,
                'color': color,
                'badge_name': badge,
                'occupation': 'Teacher'
            }
            likes = Like.query.filter(Like.user_id == teacher.id, Like.user_type == 0).all()
            like_list = []
            for like in likes:
                skill = Skills.query.filter(Skills.skill_id == like.skill_id).first()
                like_list.append({
                    'skill_name': skill.skill_name,
                    'like_num': skill.like
                })
            if form.validate_on_submit():
                teacher_in_db = Teacher.query.filter(Teacher.email == email).first()
                teacher_in_db.firstname = form.firstname.data
                teacher_in_db.lastname = form.lastname.data
                teacher_in_db.phone = form.phone.data
                teacher_in_db.school = form.school.data
                db.session.add(teacher_in_db)
                db.session.commit()
                session.clear()
                flash('Information has been updated')
                return redirect(url_for('signin'))
    else:
        flash("Please sign in first")
        return redirect(url_for('signin'))
    session['EMAIL'] = email
    return render_template('profile.html', user=user_info, form=form, skill_list=json.dumps(skill_statistic),
                           topic_master=topic_master_dict, score_list=score_list, unit_score=None, likes=like_list,
                           subscribers=subscribers, following=following)


@app.route('/profile_collections', methods=['GET', 'POST'])
def profile_collections():
    email = session.get('EMAIL')
    student = Student.query.filter(Student.email == email).first()
    teacher = Teacher.query.filter(Teacher.email == email).first()
    user_info = ''
    if student:
        name = student.lastname
        image = open('static/images/icon/' + student.profile_photo + ".png", 'rb')
        img_stream = image.read()
        img_stream = base64.b64encode(img_stream).decode('ascii')
        avatars = Avatar.query.filter(Avatar.user_id == student.id, Avatar.user_type == 1).all()
        badges = Badge.query.filter(Badge.user_id == student.id, Badge.user_type == 1).all()
        if student.badge_name:
            color = student.badge_name.split('_')[1]
            badge = base64.b64encode(open('static/images/badge/' + student.badge_name + ".png", 'rb').read()).decode(
                'ascii')
        else:
            color = None
            badge = None
        user_info = {
            'email': email,
            'coins': student.coins,
            'first_name': student.firstname,
            'last_name': student.lastname,
            'profile_pic': img_stream,
            'phone': student.phone,
            'school': student.school,
            'address': student.address,
            'age': datetime.now().date().year - int(student.dob.split("-")[0]),
            'gender': student.gender,
            'password': student.password,
            'color': color,
            'badge_name': badge,
            'time_capsule1': student.time_capsule1,
            'time_capsule2': student.time_capsule2,
            'occupation': 'Student'
        }
    elif teacher:
        image = open('static/images/icon/' + teacher.profile_photo + ".png", 'rb')
        img_stream = image.read()
        img_stream = base64.b64encode(img_stream).decode('ascii')
        avatars = Avatar.query.filter(Avatar.user_id == teacher.id, Avatar.user_type == 0).all()
        badges = Badge.query.filter(Badge.user_id == teacher.id, Badge.user_type == 0).all()
        if teacher.badge_name:
            color = teacher.badge_name.split('_')[1]
            badge = base64.b64encode(open('static/images/badge/' + teacher.badge_name + ".png", 'rb').read()).decode(
                'ascii')
        else:
            color = None
            badge = None
        user_info = {
            'email': email,
            'first_name': teacher.firstname,
            'coins': teacher.coins,
            'last_name': teacher.lastname,
            'profile_pic': img_stream,
            'phone': teacher.phone,
            'school': teacher.school,
            'password': teacher.password,
            'color': color,
            'badge_name': badge,
            'time_capsule1': teacher.time_capsule1,
            'time_capsule2': teacher.time_capsule2,
            'occupation': 'Teacher'
        }
    return render_template('profile_collections.html', user=user_info, skill_list=None,
                           topic_master=None, score_list=None, unit_score=None, avatars=avatars, badges=badges,
                           cap1=user_info['time_capsule1'], cap2=user_info['time_capsule2'])


@app.route('/user_collections/<user_email>', methods=['GET', 'POST'])
def user_collections(user_email):
    email = session.get('EMAIL')
    name = session.get('NAME')
    if name:
        session['NAME'] = name
        session['EMAIL'] = email
        me_student = Student.query.filter(Student.email == email).first()
        me_teacher = Teacher.query.filter(Teacher.email == email).first()
        me = ''
        if me_student:
            me = me_student
            occupation = 'Student'
        if me_teacher:
            me = me_teacher
            occupation = 'Teacher'
        me_i = open('static/images/icon/' + me.profile_photo + ".png", 'rb')
        me_img = me_i.read()
        me_img = base64.b64encode(me_img).decode('ascii')
        if me.badge_name:
            color = me.badge_name.split('_')[1]
            badge = base64.b64encode(open('static/images/badge/' + me.badge_name + ".png", 'rb').read()).decode(
                'ascii')
        else:
            color = None
            badge = None
        my_info = {
            'email': email,
            'first_name': me.firstname,
            'last_name': me.lastname,
            'color': color,
            'badge_name': badge,
            'profile_pic': me_img,
            'occupation': occupation
        }
        student = Student.query.filter(Student.email == user_email).first()
        teacher = Teacher.query.filter(Teacher.email == user_email).first()
        user_info = ''
        if student:
            image = open('static/images/icon/' + student.profile_photo + ".png", 'rb')
            img_stream = image.read()
            img_stream = base64.b64encode(img_stream).decode('ascii')
            avatars = Avatar.query.filter(Avatar.user_id == student.id, Avatar.user_type == 1).all()
            badges = Badge.query.filter(Badge.user_id == student.id, Badge.user_type == 1).all()
            if student.badge_name:
                color = student.badge_name.split('_')[1]
                badge = base64.b64encode(open('static/images/badge/' + student.badge_name + ".png", 'rb').read()).decode(
                    'ascii')
            else:
                color = None
                badge = None
            user_info = {
                'email': user_email,
                'coins': student.coins,
                'first_name': student.firstname,
                'last_name': student.lastname,
                'profile_pic': img_stream,
                'phone': student.phone,
                'school': student.school,
                'address': student.address,
                'age': datetime.now().date().year - int(student.dob.split("-")[0]),
                'gender': student.gender,
                'password': student.password,
                'color': color,
                'badge_name': badge,
                'time_capsule1': student.time_capsule1,
                'time_capsule2': student.time_capsule2,
                'occupation': 'Student'
            }
        elif teacher:
            image = open('static/images/icon/' + teacher.profile_photo + ".png", 'rb')
            img_stream = image.read()
            img_stream = base64.b64encode(img_stream).decode('ascii')
            avatars = Avatar.query.filter(Avatar.user_id == teacher.id, Avatar.user_type == 0).all()
            badges = Badge.query.filter(Badge.user_id == teacher.id, Badge.user_type == 0).all()
            if teacher.badge_name:
                color = teacher.badge_name.split('_')[1]
                badge = base64.b64encode(open('static/images/badge/' + teacher.badge_name + ".png", 'rb').read()).decode(
                    'ascii')
            else:
                color = None
                badge = None
            user_info = {
                'email': user_email,
                'first_name': teacher.firstname,
                'coins': teacher.coins,
                'last_name': teacher.lastname,
                'profile_pic': img_stream,
                'phone': teacher.phone,
                'school': teacher.school,
                'password': teacher.password,
                'color': color,
                'badge_name': badge,
                'time_capsule1': teacher.time_capsule1,
                'time_capsule2': teacher.time_capsule2,
                'occupation': 'Teacher'
            }
    else:
        flash("Please sign in first")
        return redirect(url_for('signin'))
    return render_template('user_collections.html', user=my_info, user_info=user_info, skill_list=None,
                           topic_master=None, score_list=None, unit_score=None, avatars=avatars, badges=badges,
                           cap1=user_info['time_capsule1'], cap2=user_info['time_capsule2'])


@app.route('/change_profile/<email>', methods=['GET', 'POST'])
def change_profile(email):
    from models import db
    student = Student.query.filter(Student.email == email).first()
    teacher = Teacher.query.filter(Teacher.email == email).first()
    type = request.form.get("type")
    if type == 'photo':
        if student:
            if request.form.get("photo") == 'Default':
                student.profile_photo = student.lastname[0]
                db.session.add(student)
                db.session.commit()
            else:
                student.profile_photo = request.form.get("photo")
                db.session.add(student)
                db.session.commit()
        if teacher:
            if request.form.get("photo") == 'Default':
                teacher.profile_photo = teacher.lastname[0]
                db.session.add(teacher)
                db.session.commit()
            else:
                teacher.profile_photo = request.form.get("photo")
                db.session.add(teacher)
                db.session.commit()
    if type == 'badge':
        if student:
            if request.form.get("photo") == 'Default':
                student.badge_name = None
                db.session.add(student)
                db.session.commit()
            else:
                student.badge_name = request.form.get("photo")
                db.session.add(student)
                db.session.commit()
        if teacher:
            if request.form.get("photo") == 'Default':
                teacher.badge_name = None
                db.session.add(teacher)
                db.session.commit()
            else:
                teacher.badge_name = request.form.get("photo")
                db.session.add(teacher)
                db.session.commit()
    return 'result'


@app.route('/grade/<topic_name>', methods=['GET', 'POST'])
def grade(topic_name):
    email = session.get('EMAIL')
    student = Student.query.filter(Student.email == email).first()
    _, skill_statistic, _ = return_score(student)
    image = open('static/images/icon/' + student.profile_photo + ".png", 'rb')
    img_stream = image.read()
    img_stream = base64.b64encode(img_stream).decode('ascii')
    if student.badge_name:
        color = student.badge_name.split('_')[1]
        badge = base64.b64encode(open('static/images/badge/' + student.badge_name + ".png", 'rb').read()).decode(
            'ascii')
    else:
        color = None
        badge = None
    user_info = {
        'email': email,
        'first_name': student.firstname,
        'last_name': student.lastname,
        'profile_pic': img_stream,
        'phone': student.phone,
        'school': student.school,
        'address': student.address,
        'age': datetime.now().date().year - int(student.dob.split("-")[0]),
        'gender': student.gender,
        'password': student.password,
        'color': color,
        'badge_name': badge,
        'occupation': 'Student'
    }
    topic = Topics.query.filter(Topics.topic_name == topic_name).first()
    skills = Skills.query.filter(Skills.topic_id == topic.topic_id).all()
    skill_score_list = []
    for skill in skills:
        scores = Score.query.filter(Score.student_id == student.id, Score.skill_id == skill.skill_id).order_by(
            Score.date.asc()).all()
        skill_name = skill.skill_name
        score_list = {}
        for score in scores:
            score_list[str(score.date)] = score.score
        skill_score_list.append({
            'skill_name': skill_name,
            'score_list': list(score_list.values()),
            'date': list(score_list.keys())
        })
    return render_template('grade.html', user=user_info, score_list=json.dumps(skill_score_list),
                           skill_score_list=skill_score_list, skill_list=json.dumps(skill_statistic), unit_score=None)


@app.route('/user_grade/<user_email>/<topic_name>', methods=['GET', 'POST'])
def user_grade(user_email, topic_name):
    email = session.get('EMAIL')
    name = session.get('NAME')
    if name:
        session['NAME'] = name
        session['EMAIL'] = email
        me_student = Student.query.filter(Student.email == email).first()
        me_teacher = Teacher.query.filter(Teacher.email == email).first()
        me = ''
        if me_student:
            me = me_student
            occupation = 'Student'
        if me_teacher:
            me = me_teacher
            occupation = 'Teacher'
        me_i = open('static/images/icon/' + me.profile_photo + ".png", 'rb')
        me_img = me_i.read()
        me_img = base64.b64encode(me_img).decode('ascii')
        if me.badge_name:
            color = me.badge_name.split('_')[1]
            badge = base64.b64encode(open('static/images/badge/' + me.badge_name + ".png", 'rb').read()).decode(
                'ascii')
        else:
            color = None
            badge = None
        my_info = {
            'email': email,
            'first_name': me.firstname,
            'last_name': me.lastname,
            'color': color,
            'badge_name': badge,
            'profile_pic': me_img,
            'occupation': occupation
        }
        student = Student.query.filter(Student.email == user_email).first()
        _, skill_statistic, _ = return_score(student)
        image = open('static/images/icon/' + student.profile_photo + ".png", 'rb')
        img_stream = image.read()
        img_stream = base64.b64encode(img_stream).decode('ascii')
        if student.badge_name:
            color = student.badge_name.split('_')[1]
            badge = base64.b64encode(open('static/images/badge/' + student.badge_name + ".png", 'rb').read()).decode(
                'ascii')
        else:
            color = None
            badge = None
        user_info = {
            'email': user_email,
            'first_name': student.firstname,
            'last_name': student.lastname,
            'profile_pic': img_stream,
            'phone': student.phone,
            'school': student.school,
            'address': student.address,
            'age': datetime.now().date().year - int(student.dob.split("-")[0]),
            'gender': student.gender,
            'password': student.password,
            'color': color,
            'badge_name': badge,
            'occupation': 'Student'
        }
        topic = Topics.query.filter(Topics.topic_name == topic_name).first()
        skills = Skills.query.filter(Skills.topic_id == topic.topic_id).all()
        skill_score_list = []
        for skill in skills:
            scores = Score.query.filter(Score.student_id == student.id, Score.skill_id == skill.skill_id).order_by(
                Score.date.asc()).all()
            skill_name = skill.skill_name
            score_list = {}
            for score in scores:
                score_list[str(score.date)] = score.score
            skill_score_list.append({
                'skill_name': skill_name,
                'score_list': list(score_list.values()),
                'date': list(score_list.keys())
            })
    else:
        flash("Please sign in first")
        return redirect(url_for('signin'))
    print(user_info['email'])
    return render_template('user_grade.html', user=my_info, user_info=user_info, score_list=json.dumps(skill_score_list),
                           skill_score_list=skill_score_list, skill_list=json.dumps(skill_statistic), unit_score=None)


@app.route('/unit_grade', methods=['GET', 'POST'])
def unit_grade():
    email = session.get('EMAIL')
    student = Student.query.filter(Student.email == email).first()
    _, skill_statistic, _ = return_score(student)
    image = open('static/images/icon/' + student.profile_photo + ".png", 'rb')
    img_stream = image.read()
    img_stream = base64.b64encode(img_stream).decode('ascii')
    if student.badge_name:
        color = student.badge_name.split('_')[1]
        badge = base64.b64encode(open('static/images/badge/' + student.badge_name + ".png", 'rb').read()).decode(
            'ascii')
    else:
        color = None
        badge = None
    user_info = {
        'email': email,
        'first_name': student.firstname,
        'last_name': student.lastname,
        'profile_pic': img_stream,
        'phone': student.phone,
        'school': student.school,
        'address': student.address,
        'age': datetime.now().date().year - int(student.dob.split("-")[0]),
        'gender': student.gender,
        'password': student.password,
        'color': color,
        'badge_name': badge,
        'occupation': 'Student'
    }
    unit_score = []
    units = Unit.query.filter(Unit.student_id == student.id).all()
    print(units)
    unit_dict = {}
    topics = Topics.query.filter().all()
    for topic in topics:
        unit_dict[topic.topic_name] = collections.deque()
    for unit in units:
        topic_name = Topics.query.filter(Topics.topic_id == unit.topic_id).first().topic_name
        unit_dict[topic_name].append(unit.score)
        if len(unit_dict[topic_name]) < 6:
            unit_dict[topic_name].appendleft(0)
        if len(unit_dict[topic_name]) >= 6:
            unit_dict[topic_name].popleft()
    color = ["#ff6384", "#4bc0c0", "#ffcd56",
             "#07b107", "#36a2eb"]
    idx = 0
    max_len = max([len(l) for l in unit_dict.values()])
    for unit, score_list in unit_dict.items():
        unit_score.append({
            'data': list(score_list),
            'label': unit,
            'borderColor': color[idx],
        })
        idx+=1
    print(unit_score)
    return render_template('unit_grade.html', user=user_info, score_list=None,
                           skill_score_list=None, skill_list=None, unit_score=json.dumps(unit_score), max_len=max_len)

@app.route('/user_unit_grade/<user_email>', methods=['GET', 'POST'])
def user_unit_grade(user_email):
    email = session.get('EMAIL')
    name = session.get('NAME')
    if name:
        session['NAME'] = name
        session['EMAIL'] = email
        me_student = Student.query.filter(Student.email == email).first()
        me_teacher = Teacher.query.filter(Teacher.email == email).first()
        me = ''
        if me_student:
            me = me_student
            occupation = 'Student'
        if me_teacher:
            me = me_teacher
            occupation = 'Teacher'
        me_i = open('static/images/icon/' + me.profile_photo + ".png", 'rb')
        me_img = me_i.read()
        me_img = base64.b64encode(me_img).decode('ascii')
        if me.badge_name:
            color = me.badge_name.split('_')[1]
            badge = base64.b64encode(open('static/images/badge/' + me.badge_name + ".png", 'rb').read()).decode(
                'ascii')
        else:
            color = None
            badge = None
        my_info = {
            'email': email,
            'first_name': me.firstname,
            'last_name': me.lastname,
            'color': color,
            'badge_name': badge,
            'profile_pic': me_img,
            'occupation': occupation
        }
        user_unit_score = []
        user_student = Student.query.filter(Student.email == user_email).first()
        image = open('static/images/icon/' + user_student.profile_photo + ".png", 'rb')
        img_stream = image.read()
        img_stream = base64.b64encode(img_stream).decode('ascii')

        if user_student.badge_name:
            color = user_student.badge_name.split('_')[1]
            badge = base64.b64encode(open('static/images/badge/' + user_student.badge_name + ".png", 'rb').read()).decode(
                'ascii')
        else:
            color = None
            badge = None
        user_info = {
            'email': user_email,
            'coins': user_student.coins,
            'first_name': user_student.firstname,
            'last_name': user_student.lastname,
            'profile_pic': img_stream,
            'phone': user_student.phone,
            'school': user_student.school,
            'address': user_student.address,
            'age': datetime.now().date().year - int(user_student.dob.split("-")[0]),
            'gender': user_student.gender,
            'password': user_student.password,
            'color': color,
            'badge_name': badge,
            'time_capsule1': user_student.time_capsule1,
            'time_capsule2': user_student.time_capsule2,
            'occupation': 'Student'
        }
        units = Unit.query.filter(Unit.student_id == user_student.id).all()
        unit_dict = {}
        topics = Topics.query.filter().all()
        for topic in topics:
            unit_dict[topic.topic_name] = collections.deque()
        for unit in units:
            topic_name = Topics.query.filter(Topics.topic_id == unit.topic_id).first().topic_name
            unit_dict[topic_name].append(unit.score)
            if len(unit_dict[topic_name]) < 6:
                unit_dict[topic_name].appendleft(0)
            if len(unit_dict[topic_name]) >= 6:
                unit_dict[topic_name].popleft()
        color = ["#ff6384", "#4bc0c0", "#ffcd56",
                 "#07b107", "#36a2eb"]
        idx = 0
        max_len = max([len(l) for l in unit_dict.values()])
        for unit, score_list in unit_dict.items():
            user_unit_score.append({
                'data': list(score_list),
                'label': unit,
                'borderColor': color[idx],
            })
            idx+=1
        print(user_info)
    else:
        flash("Please sign in first")
        return redirect(url_for('signin'))
    return render_template('user_unit_grade.html', user=my_info, user_info=user_info, score_list=None,
                           skill_score_list=None, skill_list=None, unit_score=json.dumps(user_unit_score), max_len=max_len)


if __name__ == '__main__':
    app.run(debug=True)

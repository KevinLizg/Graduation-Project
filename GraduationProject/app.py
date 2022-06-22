import base64
import itertools
import os
import random, json
import urllib

import wolframalpha
import xmltodict
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
    # user_type = session.get('ACTOR')
    # name = ''
    # if email and user_type == 'Student':
    #     student = Student.query.filter(Student.student_email == email).first()
    #     name = student.firstname
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
    if form.validate_on_submit() and form.token.data == '123':
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
    elif form.token.data != '123':
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
    print(user_type)
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
    try:
        email = s.loads(token, salt='email-confirm', max_age=180)
        if form.validate_on_submit():
            if form.firstname.data.isalpha() and form.lastname.data.isalpha():
                passw_hash = generate_password_hash(form.password.data)
                student = Student(email=email, firstname=form.firstname.data, lastname=form.lastname.data,
                                  password=passw_hash, gender=form.gender.data, phone=form.phone.data,
                                  school=form.school.data, dob=form.dob.data, address=form.address.data)
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
                teacher = Teacher(email=email, firstname=form.firstname.data, lastname=form.lastname.data,
                                  password=passw_hash, phone=form.phone.data,
                                  school=form.school.data)
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
    return render_template('topics.html', name=name, topic=topic, skills=paginate.items, paginate=paginate, info=info,
                           comment_info=comment_info, all_topic=topic_info)


@app.route('/skill_details/<skill_>', methods=['GET', 'POST'])
def skill_details(skill_):
    name = session.get('NAME')
    email = session.get('EMAIL')
    if(name):
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
        print(user_in_db.id)
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
                image = open('static/images/icon/' + reply_user.lastname[0] + ".png", 'rb')
                img_stream = image.read()
                img_stream = base64.b64encode(img_stream).decode('ascii')
                reply_list.append({
                    'reply_content': reply.reply_content,
                    'reply_user_name': reply_user.firstname + ', ' + reply_user.lastname,
                    'reply_time': reply.reply_time,
                    'reply_img': img_stream
                })
            image = open('static/images/icon/' + user.lastname[0] + ".png", 'rb')
            img_stream = image.read()
            img_stream = base64.b64encode(img_stream).decode('ascii')
            comments.append({
                'comment_id': comment.comment_id,
                'comment': comment.comment,
                'user_name': user.firstname + ', ' + user.lastname,
                'user_email': user.email,
                'comment_time': comment.comment_time,
                'replies': reply_list,
                'user_img': img_stream
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
                           commentForm=commentForm,
                           name=name, email=email, all_skill=all_skill,
                           paginate=paginate, comment_count=comment_count, like=like
                           )


@app.route('/ready/<skill_>', methods=["GET", "POST"])
def ready(skill_):
    name = session.get('NAME')
    email = session.get('EMAIL')
    print(skill_)
    print(email)
    if (name):
        session['NAME'] = name
        session['EMAIL'] = email
    else:
        flash("Please sign in first")
        return redirect(url_for('signin'))
    return render_template("ready.html", filename=email+".json", name=name, email=email, skill_=skill_)


@app.route('/practice/<skill_>')
def practice(skill_):
    name = session.get('NAME')
    email = session.get('EMAIL')
    if (name):
        session['NAME'] = name
        session['EMAIL'] = email
        user = Student.query.filter(Student.email == email).first()
        skill = Skills.query.filter(Skills.skill_name == skill_).first()
        list = []
        coins = 50
        for i in range(0, 5):
            problem = ''
            solution = ''
            if skill.skill_id == 1:
                ran_num = random.randint(0, 1)
                if ran_num == 0:
                    problem, solution = mathgen.genById(0)
                else:
                    problem, solution = mathgen.genById(1)
            app_id = 'XQAUEU-WR3AY23332'
            client = wolframalpha.Client(app_id)
            res = client.query(problem)
            img_list = []
            solution_list = []
            for pod in res.pods:
                for sub in pod.subpods:
                    img_list.append(sub.img['@src'])
                    solution_list.append(sub.plaintext)
            option_list = []
            option_list.append(str(random.randint(int(solution)-10,int(solution)-1)))
            option_list.append(str(random.randint(int(solution)+1,int(solution)+10)))
            option_list.append(str(random.randint(int(solution)+5,int(solution)+20)))
            option_list.append(solution)
            random.shuffle(option_list)
            answer = ["A", "B", "C", "D"]
            idx = 0
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
        with open('static/json/'+email+'.json', 'w', encoding='utf-8') as f:
            json.dump(list, f, ensure_ascii=False, indent=4)
    else:
        flash("Please sign in first")
        return redirect(url_for('signin'))
    return render_template('practice.html', num=1*120, name=name, email=email, coins=user.coins, skill_=skill_)


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

@app.route('/quiz/<skill_>')
def quiz(skill_):
    name = session.get('NAME')
    email = session.get('EMAIL')
    if (name):
        session['NAME'] = name
        session['EMAIL'] = email
        user = Student.query.filter(Student.email == email).first()
        skill = Skills.query.filter(Skills.skill_name == skill_).first()
        list = []
        skill_dict = {
            1: [0,1],
            2: [2,3],
            3: [6,8],
            4: [13,16,28],
            5: [53],
            6: [11],
            7: [21],
            8: [26],
            9: [24],
            10: [50],
            11: [111],
            12: [18,19,22,25],
            13: [32,33,34,38],
            14: [35,36,37,39],
            15: [112,75,115],
            16: [114],
            17: [30,42],
            18: [59],
            19: [40],
            20: [101,102],
            21: [27],
            22: [55],
        }
        # for i in range(0, 10):
        #     ran_num = random.randint(0,len(skill_dict[skill.skill_id])-1)
        #     problem, solution = mathgen.genById(skill_dict[skill.skill_id][ran_num])
        #     app_id = 'XQAUEU-WR3AY23332'
        #     client = wolframalpha.Client(app_id)
        #     # res = client.query(problem)
        #     res = query(problem, app_id)
        #     img_list = []
        #     solution_list = []
        #     for pod in res.pods:
        #         for sub in pod.subpods:
        #             img_list.append(sub.img['@src'])
        #             solution_list.append(sub.plaintext)
        #             print(sub)
        #     option_list = [solution]
        #     for j in range(1,4):
        #         gen_problem, gen_solution = mathgen.genById(skill_dict[skill.skill_id][ran_num])
        #         option_list.append(gen_solution)
        #     random.shuffle(option_list)
        #     answer = ["A", "B", "C", "D"]
        #     idx = 0
        #     for op in option_list:
        #         if op == solution:
        #             an = answer[idx]
        #         idx += 1
        #     list.append({
        #         'id': i,
        #         'title': problem,
        #         'option': option_list,
        #         'answer': an,
        #         'analysis': img_list
        #     })
        # with open('static/json/'+email+'.json', 'w', encoding='utf-8') as f:
        #     json.dump(list, f, ensure_ascii=False, indent=4)
    else:
        flash("Please sign in first")
        return redirect(url_for('signin'))
    return render_template('quiz.html', num=1*2000, name=name, email=email, coins=user.coins, skill_=skill_)


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
    like = Like.query.filter(Like.user_type == user_type, Like.skill_id == skill.skill_id, Like.user_id == user.id).first()
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
        coins = request.form.get("coins")
        student.coins = int(coins)
        db.session.add(student)
        db.session.commit()
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
        print(coins, email, skill, score)
        student = Student.query.filter(Student.email == email).first()
        skill = Skills.query.filter(Skills.skill_name == skill).first()
        score_add = Score(student_id=student.id, skill_id=skill.skill_id, score=score, time=time)
        db.session.add(score_add)
        db.session.commit()
        # if scores:
        #     for sc in scores:
        #         skill = Skills.query.filter(Skills.skill_name == skill).first()
        #         if sc.skill_id == skill.skill_id:
        #             sc.total_score = sc.total_score + int(score)
        #             sc.number_times += 1
        #             db.session.add(sc)
        #             db.session.commit()
        #         else:
        #             score_add = Score(student_id=student.id, skill_id=skill.skill_id, total_score=sc.total_score + int(score),
        #                               number_times=sc.number_times + 1)
        #             db.session.add(score_add)
        #             db.session.commit()
        # else:
        #     skill = Skills.query.filter(Skills.skill_name == skill).first()
        #     score_add = Score(student_id=student.id, skill_id=skill.skill_id, total_score=score, number_times=1)
        #     db.session.add(score_add)
        #     db.session.commit()
        student.coins = int(coins)
        db.session.add(student)
        db.session.commit()
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
    session['NAME'] = name
    session['EMAIL'] = email
    user_email = user_email
    student = Student.query.filter(Student.email == user_email).first()
    teacher = Teacher.query.filter(Teacher.email == user_email).first()
    me_student = Student.query.filter(Student.email == email).first()
    me_teacher = Teacher.query.filter(Teacher.email == email).first()
    me = ''
    if me_student:
        me = me_student
    if me_teacher:
        me = me_teacher
    me_i = open('static/images/icon/' + me.lastname[0] + ".png", 'rb')
    me_img = me_i.read()
    me_img = base64.b64encode(me_img).decode('ascii')
    my_info = {
            'email': email,
            'first_name': me.firstname,
            'last_name': me.lastname,
            'profile_pic': me_img,
        }
    if student:
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
                'topic': t_name,
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
        student_name = student.lastname
        image = open('static/images/icon/' + student_name[0] + ".png", 'rb')
        img_stream = image.read()
        img_stream = base64.b64encode(img_stream).decode('ascii')
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
            'occupation': 'Student'
        }
    elif teacher:
        skill_statistic = {}
        topic_master_dict = {}
        score_list = []
        form = TeacherUpdateInfo()
        name = teacher.lastname
        image = open('static/images/icon/' + name[0] + ".png", 'rb')
        img_stream = image.read()
        img_stream = base64.b64encode(img_stream).decode('ascii')
        user_info = {
            'email': user_email,
            'first_name': teacher.firstname,
            'last_name': teacher.lastname,
            'profile_pic': img_stream,
            'phone': teacher.phone,
            'school': teacher.school,
            'password': teacher.password,
            'occupation': 'Teacher'
        }
    return render_template('user_profile.html', name=name, email=email, user=user_info, skill_list=json.dumps(skill_statistic),
                           topic_master=topic_master_dict, score_list=score_list, my_info=my_info)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    from models import db
    email = session.get('EMAIL')
    student = Student.query.filter(Student.email == email).first()
    teacher = Teacher.query.filter(Teacher.email == email).first()
    if student:
        student = Student.query.filter(Student.email == email).first()
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
                'topic': t_name,
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
            topic_master_dict[k] = int(topic_master_dict[k]/topic_master_count[k])
        skill_statistic = {
            'skill_list': list(skill_name_dict.keys()),
            'skill_value_list': list(skill_name_dict.values()),
        }
        form = UpdateInfo()
        # if student.agent_photo != None:
        #     image = open(os.path.join(app.config['UPLOAD_PATH'], student.agent_photo), 'rb')
        #     img_stream = image.read()
        #     img_stream = base64.b64encode(img_stream).decode('ascii')
        # else:
        name = student.lastname
        image = open('static/images/icon/' + name[0] + ".png", 'rb')
        img_stream = image.read()
        img_stream = base64.b64encode(img_stream).decode('ascii')
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
            'occupation': 'Student'
        }
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
        skill_statistic = {}
        topic_master_dict = {}
        score_list = []
        form = TeacherUpdateInfo()
        name = teacher.lastname
        image = open('static/images/icon/' + name[0] + ".png", 'rb')
        img_stream = image.read()
        img_stream = base64.b64encode(img_stream).decode('ascii')
        user_info = {
            'email': email,
            'first_name': teacher.firstname,
            'last_name': teacher.lastname,
            'profile_pic': img_stream,
            'phone': teacher.phone,
            'school': teacher.school,
            'password': teacher.password,
            'occupation': 'Teacher'
        }
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
    session['EMAIL'] = email
    return render_template('profile.html', user=user_info, form=form, skill_list=json.dumps(skill_statistic),
                           topic_master=topic_master_dict, score_list=score_list)



@app.route('/testchart', methods=['GET', 'POST'])
def testchart():
    return render_template('testchart.html')


if __name__ == '__main__':
    app.run(debug=True)

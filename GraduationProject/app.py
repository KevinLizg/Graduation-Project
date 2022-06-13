import base64
import os
import random, json

import wolframalpha
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
        student_in_db = Student.query.filter(Student.email == email).first()
        teacher_in_db = Teacher.query.filter(Teacher.email == email).first()
        if student_in_db:
            user_in_db = student_in_db
            user_type = 1
        elif teacher_in_db:
            user_in_db = teacher_in_db
            user_type = 0
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 3))
        paginate = Comments.query.filter(Comments.skill_id == skill.skill_id).order_by(
            Comments.comment_time.desc()).paginate(page, per_page, error_out=False)
        comment_count = Comments.query.filter(Comments.skill_id == skill.skill_id).count()
        for comment in paginate.items:
            user = ''
            if comment.user_type == True:
                user = Student.query.filter(Student.id == comment.user_id).first()
            elif comment.user_type == False:
                user = Teacher.query.filter(Teacher.id == comment.user_id).first()
            reply_list = []
            replies = Reply.query.filter(Reply.comment_id == comment.comment_id).all()
            for reply in replies:
                if reply.user_type == True:
                    reply_user = Student.query.filter(Student.id == comment.user_id).first()
                elif reply.user_type == False:
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
        print(comment_count)
    else:
        flash("Please sign in first")
        return redirect(url_for('signin'))
    return render_template('skill_details.html', skill=skill, comments=comments, replyForm=replyForm,
                           commentForm=commentForm,
                           name=name, email=email, all_skill=all_skill,
                           paginate=paginate, comment_count=comment_count
                           )


@app.route('/ready', methods=["GET", "POST"])
def ready():
    name = session.get('NAME')
    email = session.get('EMAIL')
    if (name):
        session['NAME'] = name
        session['EMAIL'] = email
    else:
        flash("Please sign in first")
        return redirect(url_for('signin'))
    return render_template("ready.html", filename=email+".json")


@app.route('/quiz')
def quiz():
    name = session.get('NAME')
    email = session.get('EMAIL')
    if (name):
        session['NAME'] = name
        session['EMAIL'] = email
        list = []
        for i in range(0, 5):
            ran_num = random.randint(0, 1)
            if (ran_num == 0):
                problem, solution = mathgen.genById(0)
            else:
                problem, solution = mathgen.genById(1)
        #     app_id = 'XQAUEU-WR3AY23332'
        #     client = wolframalpha.Client(app_id)
        #     res = client.query(problem)
        #     print(problem)
        #     img_list = []
        #     solution_list = []
        #     for pod in res.pods:
        #         for sub in pod.subpods:
        #             img_list.append(sub.img['@src'])
        #             solution_list.append(sub.plaintext)
        #     option_list = []
        #     option_list.append(str(random.randint(int(solution)-10,int(solution)-1)))
        #     option_list.append(str(random.randint(int(solution)+1,int(solution)+10)))
        #     option_list.append(str(random.randint(int(solution)+5,int(solution)+20)))
        #     option_list.append(solution)
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
    return render_template('quiz.html', num=1 * 5,name=name, email=email, type="shit")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return render_template('index.html')


@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('test.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    from models import db
    email = session.get('EMAIL')
    student = Student.query.filter(Student.email == email).first()
    teacher = Teacher.query.filter(Teacher.email == email).first()
    if student:
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
    return render_template('profile.html', user=user_info, form=form)


if __name__ == '__main__':
    app.run(debug=True)

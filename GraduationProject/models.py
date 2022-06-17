from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True)
    firstname = db.Column(db.String(128))
    lastname = db.Column(db.String(128))
    dob = db.Column(db.String(128))
    password = db.Column(db.String(128))
    gender = db.Column(db.String(128))
    phone = db.Column(db.String(128))
    address = db.Column(db.String(128))
    school = db.Column(db.String(128))
    coins = db.Column(db.Integer())


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True)
    firstname = db.Column(db.String(128))
    lastname = db.Column(db.String(128))
    password = db.Column(db.String(128))
    phone = db.Column(db.String(128), index=True, unique=True)
    school = db.Column(db.String(128), index=True, unique=True)


class Topics(db.Model):
    topic_id = db.Column(db.Integer, primary_key=True)
    topic_name = db.Column(db.String(128), index=True, unique=True)


class Skills(db.Model):
    skill_id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(128), nullable=True)
    skill_introduction = db.Column(db.String(128), nullable=True)
    like = db.Column(db.String(128))
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.topic_id'))


class Comments(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(128), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.skill_id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('skills.topic_id'))
    user_id = db.Column(db.Integer, nullable=True)
    user_type = db.Column(db.Boolean, nullable=True)
    comment_time = db.Column(db.String(128), nullable=True)


class Reply(db.Model):
    reply_id = db.Column(db.Integer, primary_key=True)
    reply_content = db.Column(db.String(128), nullable=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.comment_id'))
    user_id = db.Column(db.Integer, nullable=True)
    user_type = db.Column(db.Boolean, nullable=True)
    reply_time = db.Column(db.String(128), nullable=True)


class Score(db.Model):
    score_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.skill_id'))
    total_score = db.Column(db.Integer)
    number_times = db.Column(db.Integer)
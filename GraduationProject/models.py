from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    student_email = db.Column(db.String(128), index=True, unique=True)
    student_firstname = db.Column(db.String(128))
    student_lastname = db.Column(db.String(128))
    student_dob = db.Column(db.String(128))
    student_password = db.Column(db.String(128))
    student_gender = db.Column(db.String(128))
    student_phone = db.Column(db.String(128))
    student_address = db.Column(db.String(128))
    student_school = db.Column(db.String(128))
    # student_level = db.Column(db.String(128))


class Teacher(db.Model):
    teacher_id = db.Column(db.Integer, primary_key=True)
    teacher_email = db.Column(db.String(128), index=True, unique=True)
    teacher_firstname = db.Column(db.String(128))
    teacher_lastname = db.Column(db.String(128))
    teacher_password = db.Column(db.String(128))
    teacher_phone = db.Column(db.String(128), index=True, unique=True)
    teacher_school = db.Column(db.String(128), index=True, unique=True)


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
    user_id = db.Column(db.Integer, nullable=True)
    user_type = db.Column(db.Boolean, nullable=True)
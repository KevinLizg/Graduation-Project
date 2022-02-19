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
    student_phone = db.Column(db.String(128), index=True, unique=True)
    student_address = db.Column(db.String(128))
    student_school = db.Column(db.String(128))
    student_level = db.Column(db.String(128))
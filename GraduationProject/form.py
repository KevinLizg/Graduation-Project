from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, RadioField, FileField, \
    SelectField, TextAreaField, MultipleFileField, validators
from wtforms.validators import DataRequired, EqualTo, Email, Length
import email_validator
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.fields.html5 import DateField
from flask_wtf.recaptcha import RecaptchaField

app = Flask(__name__)

app.config['SECRET_KEY'] = 'lablam.2017'
app.config['RECAPTCHA_USE_SSL']= False
app.config['RECAPTCHA_PUBLIC_KEY']='enter_your_public_key'
app.config['RECAPTCHA_PRIVATE_KEY']='enter_your_private_key'
app.config['RECAPTCHA_OPTIONS']= {'theme':'black'}


class EmailVeriForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='Please enter the correct Email'), Email(message='Please enter Correct Eamil')], render_kw={"placeholder": "Verify Your Email"})
    submit = SubmitField('Verify')


class TeacherEmailVeriForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='Please enter the correct Email'), Email(message='Please enter Correct Eamil')], render_kw={"placeholder": "Verify Your Email"})
    token = StringField('Token',validators=[DataRequired(message='Please enter the correct Token')], render_kw={"placeholder": "Enter Your Token"})
    submit = SubmitField('Verify')


class SignupForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(message='Please enter your first name')], render_kw={"placeholder": "First Name"})
    lastname = StringField('Last Name', validators=[DataRequired(message='Please enter your last name')], render_kw={"placeholder": "Last Name"})
    password = PasswordField('Password', validators=[DataRequired(message='Please enter your password'), Length(min=6,max=15)], render_kw={"placeholder": "Password"})
    password2 = PasswordField('Repeat Password', validators=[EqualTo('password', 'Not the same password')], render_kw={"placeholder": "Repeat Your Password"})
    phone = StringField('Phone Number', validators=[validators.Regexp('^(\d{10}|\d{11}|\d{12})$', message="Please enter a valid phone number"), DataRequired(message='Please enter your phone number'), ], render_kw={"placeholder": "Phone Number"})
    address = StringField('Your Address', validators=[ DataRequired(message='Please enter your address')], render_kw={"placeholder": "Address"})
    dob = DateField('Date of Birth', validators=[DataRequired(message='Please Select the date of birth')], render_kw={"placeholder": "Date of Birth"})
    gender = SelectField('Your Gender',
                          choices=[('Male', "Male"), ('Female', 'Female')],
                          validators=[DataRequired()], render_kw={"placeholder": "Gender"})
    # level = SelectField('Level', validators=[DataRequired(message='Please enter your Level'), ], render_kw={"placeholder": "Your level"}, choices=[('1', 'Level 1'), ('2', 'Level 2'), ('3', 'Level 3')])
    school = StringField('School', validators=[DataRequired(message='Please enter your School'), ], render_kw={"placeholder": "Your school"})
    submit = SubmitField('Sign Up')


class TeacherSignupForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(message='Please enter your first name')], render_kw={"placeholder": "First Name"})
    lastname = StringField('Last Name', validators=[DataRequired(message='Please enter your last name')], render_kw={"placeholder": "Last Name"})
    password = PasswordField('Password', validators=[DataRequired(message='Please enter your password'), Length(min=6,max=15)], render_kw={"placeholder": "Password"})
    password2 = PasswordField('Repeat Password', validators=[EqualTo('password', 'Not the same password')], render_kw={"placeholder": "Repeat Your Password"})
    phone = StringField('Phone Number', validators=[validators.Regexp('^(\d{10}|\d{11}|\d{12})$', message="Please enter a valid phone number"), DataRequired(message='Please enter your phone number'), ], render_kw={"placeholder": "Phone Number"})
    school = StringField('School', validators=[DataRequired(message='Please enter your School'), ], render_kw={"placeholder": "Your school"})
    submit = SubmitField('Sign Up')


class SigninForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='Please enter the correct Email'),
                                             Email(message='Please enter Correct Eamil')],
                        render_kw={"placeholder": "Your Email"})
    password = PasswordField('Password', validators=[DataRequired(message='Please enter your password')], render_kw={"placeholder": "Password"})
    submit = SubmitField('Sign In')


class UpdateInfo(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(message='Please enter your first name')],
                            render_kw={"placeholder": "First Name"})
    lastname = StringField('Last Name', validators=[DataRequired(message='Please enter your last name')],
                           render_kw={"placeholder": "Last Name"})
    phone = StringField('Phone Number', validators=[validators.Regexp('^(\d{10}|\d{11}|\d{12})$', message="Please enter a valid phone number"), DataRequired(message='Please enter your phone number'), ], render_kw={"placeholder": "Phone Number"})
    school = StringField('School', validators=[DataRequired(message='Please enter your School'), ], render_kw={"placeholder": "Your school"})
    address = StringField('Your Address', validators=[ DataRequired(message='Please enter your address')], render_kw={"placeholder": "Address"})
    submit = SubmitField('Update Info')


class TeacherUpdateInfo(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(message='Please enter your first name')],
                            render_kw={"placeholder": "First Name"})
    lastname = StringField('Last Name', validators=[DataRequired(message='Please enter your last name')],
                           render_kw={"placeholder": "Last Name"})
    phone = StringField('Phone Number', validators=[validators.Regexp('^(\d{10}|\d{11}|\d{12})$', message="Please enter a valid phone number"), DataRequired(message='Please enter your phone number'), ], render_kw={"placeholder": "Phone Number"})
    school = StringField('School', validators=[DataRequired(message='Please enter your School'), ], render_kw={"placeholder": "Your school"})
    submit = SubmitField('Update Info')


class ChangePassword(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired(message='Please enter your password'), Length(min=6, max=15)],
                             render_kw={"placeholder": "Password"})
    password2 = PasswordField('Repeat Password', validators=[EqualTo('password', 'Not the same password')],
                              render_kw={"placeholder": "Repeat Your Password"})
    submit = SubmitField('Change Password')
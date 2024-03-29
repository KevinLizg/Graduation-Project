from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, RadioField, FileField, \
    SelectField, TextAreaField, MultipleFileField, validators
from wtforms.validators import DataRequired, EqualTo, Email, Length
from wtforms.fields.html5 import DateField

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
    teacher = SelectField('Teacher', validators=[DataRequired(message='Please choose your teacher'), ], render_kw={"placeholder": "Your Teacher"}, choices=[])
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
    personal_message = TextAreaField('Message')
    submit = SubmitField('Update Info')


class TeacherUpdateInfo(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(message='Please enter your first name')],
                            render_kw={"placeholder": "First Name"})
    lastname = StringField('Last Name', validators=[DataRequired(message='Please enter your last name')],
                           render_kw={"placeholder": "Last Name"})
    phone = StringField('Phone Number', validators=[validators.Regexp('^(\d{10}|\d{11}|\d{12})$', message="Please enter a valid phone number"), DataRequired(message='Please enter your phone number'), ], render_kw={"placeholder": "Phone Number"})
    school = StringField('School', validators=[DataRequired(message='Please enter your School'), ], render_kw={"placeholder": "Your school"})
    personal_message = TextAreaField('Message')
    submit = SubmitField('Update Info')


class ChangePassword(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired(message='Please enter your password'), Length(min=6, max=15)],
                             render_kw={"placeholder": "Password"})
    password2 = PasswordField('Repeat Password', validators=[EqualTo('password', 'Not the same password')],
                              render_kw={"placeholder": "Repeat Your Password"})
    submit = SubmitField('Change Password')


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired(message='Please leave your comments or questions here')], render_kw={"placeholder": "Leave your comment or question here"})
    submit = SubmitField('Sumbit')


class ReplyForm(FlaskForm):
    reply = StringField('Reply', validators=[DataRequired(message='Please enter your reply')], render_kw={"placeholder": "Leave your reply"})
    comment_id = StringField('id')
    submit = SubmitField('Reply')


class ShopForm(FlaskForm):
    submit = SubmitField('Buy it!')


class EmailTo(FlaskForm):
    receiver = SelectField('To', validators=[DataRequired()], choices=[])
    subject = StringField('Subject',validators=[DataRequired(message='Please Enter Subject')],render_kw={"placeholder": "Subject"})
    content = TextAreaField('Content', validators=[DataRequired(message='Please Enter The Content')])
    submit = SubmitField('Send')


class EmailReplyForm(FlaskForm):
    reply = TextAreaField('Reply', validators=[DataRequired(message='Please Enter This Field')],
                          render_kw={"placeholder": "Reply"})
    submit = SubmitField('Send')
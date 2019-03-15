from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Required
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.fields.html5 import DateTimeField, DateTimeLocalField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import User
from app.models import Rfid

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class SimulateSwipeForm(FlaskForm):
    rfid = TextAreaField('RFID', validators=[DataRequired()])
    #time = TextAreaField('Time', validators=[Length(min=0, max=140)])
    time = DateTimeLocalField('Time when swiped', format='%Y-%m-%dT%H:%M')
    submit = SubmitField('Simulate Swipe')



class CreateRFIDForm(FlaskForm):
    rftagid = TextAreaField('RF TAG ID', validators=[DataRequired()])
    user_list = QuerySelectField(query_factory=lambda: User.query.all(),
                                  get_label="username")
    submit = SubmitField('Create Rfid')


class RfidAssignForm(FlaskForm):
    """
    Form for admin to rfid tags to users
    """
    user_list = QuerySelectField(query_factory=lambda: User.query.all(),
                                  get_label="username")
    rfid = QuerySelectField(query_factory=lambda: Rfid.query.all(),
                            get_label="rftagid")
    submit = SubmitField('Submit')

 
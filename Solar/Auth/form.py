from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,EmailField,RadioField
from wtforms.validators import DataRequired
from wtforms import  SubmitField


class RegistrationForm(FlaskForm):
    name=StringField('Name', validators=[DataRequired()])
    email=EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()]) 
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email=EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ForgotPasswordForm(FlaskForm):
    email=EmailField('Enter Mail')
    submit=SubmitField('Get Otp')

class OtpForm(FlaskForm):
    otp=StringField('Enter OTP')
    submit=SubmitField('Verify')
    
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')

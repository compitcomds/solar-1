from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField,StringField,TextAreaField,EmailField,IntegerField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Regexp

class homepageform1 (FlaskForm):
    name=StringField('name',validators=[DataRequired()])
    email=EmailField('email',validators=[DataRequired()])
    number=StringField('Phone Number', validators=[
            DataRequired(),
            Length(min=10, max=10, message='Phone number must be 10 digits'),
            Regexp('^\d+$', message='Phone number must contain only digits')
        ], render_kw={"placeholder": "Enter your phone number", "oninput": "this.value = this.value.replace(/[^0-9]/g, '').slice(0, 10);"})
    
    ameb=StringField('Average Monthly Bill',validators=[DataRequired()])
    pincode=StringField('Enter the Pincode',validators=[DataRequired()])
    submit=SubmitField('Submit')

class homepageform2(FlaskForm):
    name=StringField('name',validators=[DataRequired()])
    email=EmailField('email',validators=[DataRequired()])
    number=StringField('Phone Number', validators=[
                DataRequired(),
                Length(min=10, max=10, message='Phone number must be 10 digits'),
                Regexp('^\d+$', message='Phone number must contain only digits')
            ], render_kw={"placeholder": "Enter your phone number", "oninput": "this.value = this.value.replace(/[^0-9]/g, '').slice(0, 10);"})
    ameb=StringField('Average Monthly Bill',validators=[DataRequired()])
    pincode=StringField('Enter the Pincode',validators=[DataRequired()])
    submit=SubmitField('Submit')
    companyName=StringField('Comapany name',validators=[DataRequired()])

class contactform(FlaskForm):
    name=StringField('name',validators=[DataRequired()])
    email=EmailField('email',validators=[DataRequired()])
    number=StringField('Phone Number', validators=[
                DataRequired(),
                Length(min=10, max=10, message='Phone number must be 10 digits'),
                Regexp('^\d+$', message='Phone number must contain only digits')
            ], render_kw={"placeholder": "Enter your phone number", "oninput": "this.value = this.value.replace(/[^0-9]/g, '').slice(0, 10);"})
    subject=StringField('subject',validators=[DataRequired()])
    message=TextAreaField('message',validators=[DataRequired()])
    submit=SubmitField('Submit')


class productquery(FlaskForm):
    name=StringField('name',validators=[DataRequired()])
    email=EmailField('email',validators=[DataRequired()])
    number=StringField('Phone Number', validators=[
                DataRequired(),
                Length(min=10, max=10, message='Phone number must be 10 digits'),
                Regexp('^\d+$', message='Phone number must contain only digits')
            ], render_kw={"placeholder": "Enter your phone number", "oninput": "this.value = this.value.replace(/[^0-9]/g, '').slice(0, 10);"})
    netQty=IntegerField('NetQty',validators=[DataRequired()])
    submit=SubmitField('Submit')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,EmailField,RadioField,FileField, TextAreaField
from wtforms.validators import DataRequired
from wtforms import  SubmitField

class UploadForm(FlaskForm):
    title = StringField('Titile', validators=[DataRequired()])
    discription = TextAreaField('Description', validators=[DataRequired()])
    file = FileField('Image', validators=[DataRequired()])
    submit=SubmitField('Upload')
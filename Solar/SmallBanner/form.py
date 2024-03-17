from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,EmailField,RadioField,FileField
from wtforms.validators import DataRequired
from wtforms import  SubmitField

class UploadForm(FlaskForm):
    file = FileField('Image', validators=[DataRequired()])
    submit=SubmitField('Upload')
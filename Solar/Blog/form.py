from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField,StringField,TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

class UploadBlog(FlaskForm):
    heading = StringField('Enter the Heading', validators=[DataRequired()])
    image =FileField("Upload an Image", validators=[DataRequired(),FileAllowed(['jpg','png' , 'jpeg'])])
    para1 = TextAreaField('Enter the para 1', validators=[DataRequired()])
    para2 = TextAreaField('Enter the para 2')
    para3 = TextAreaField('Enter the para 3')
    para4 = TextAreaField('Enter the para 4')
    para5 = TextAreaField('Enter the para 5')
    submit = SubmitField('Upload Blog')

    def update(self, data):
        self.heading.data = data.get('heading', '')
        self.para1.data = data.get('para1', '')
        self.para2.data = data.get('para2', '')
        self.para3.data = data.get('para3', '')
        self.para4.data = data.get('para4', '')
        self.para5.data = data.get('para5', '')

class UpdateBlog(FlaskForm):
    heading = StringField('Enter the Heading', validators=[DataRequired()])
    para1 = TextAreaField('Enter para 1', validators=[DataRequired()])
    para2 = TextAreaField('Enter para 2')
    para3 = TextAreaField('Enter para 3')
    para4 = TextAreaField('Enter para 4')
    para5 = TextAreaField('Enter para 5')
    submit = SubmitField('Update Blog')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, DateField, validators, ValidationError,SelectField
from wtforms.fields.html5 import EmailField

class userform(FlaskForm):
    AGE=StringField('AGE',validators = [validators.DataRequired()])
    ID1 = SelectField('ID1 ' , choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')] ,validators = [validators.DataRequired()])
    ID2 = SelectField('ID2' ,choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')], validators = [validators.DataRequired()])
    ID3 = SelectField('ID3',choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')], validators = [validators.DataRequired()])
    ID4 = SelectField('ID4' , choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')],validators = [validators.DataRequired()])
    ID5 = SelectField('ID5' ,choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')], validators = [validators.DataRequired()])
   
    submit = SubmitField('Submit')

class health(FlaskForm):
    TEMPERATURE=StringField('TEMPERATURE',validators = [validators.DataRequired()])
    HEARTRATE=StringField('HEARTRATE',validators = [validators.DataRequired()])
    submit = SubmitField('Submit')

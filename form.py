from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, DateField, validators, ValidationError,SelectField
from wtforms.fields.html5 import EmailField

class userform(FlaskForm):
    ID1 = SelectField('ID1 ' , choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')] ,validators = [validators.DataRequired()])
    ID2 = SelectField('ID2' ,choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')], validators = [validators.DataRequired()])
    ID3 = SelectField('ID3',choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')])
    ID4 = SelectField('ID4' , choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')],validators = [validators.DataRequired()])
    ID5 = SelectField('ID5' ,choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')], validators = [validators.DataRequired()])
    ID6 = SelectField('ID6' , choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')],validators = [validators.DataRequired()])
    ID7 = SelectField('ID7', choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')],validators = [validators.DataRequired()])
    ID8 = SelectField('ID8' ,choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')],validators = [validators.DataRequired()])
    ID9 = SelectField('ID9', choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')])
    ID10 = SelectField('ID10' , choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')],validators = [validators.DataRequired()])
    ID11 = SelectField('ID11', choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')],validators = [validators.DataRequired()])
    ID12 = SelectField('ID12', choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')],validators = [validators.DataRequired()])
    ID13 = SelectField('ID13', choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')],validators = [validators.DataRequired()])
    ID14 = SelectField('ID14' , choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')],validators=[validators.DataRequired()])
    ID15 = SelectField('ID15', choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')],validators = [validators.DataRequired()])
    ID16 = SelectField('ID16', choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')],validators = [validators.DataRequired()])
    ID17 = SelectField('ID17', choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')],validators = [validators.DataRequired()])

    submit = SubmitField('Submit')
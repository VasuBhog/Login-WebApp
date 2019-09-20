from wtforms import Form, StringField, PasswordField, validators, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired(message=('Please enter a username'))])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Login')

class Register(Form):
    username = StringField('Username', [validators.DataRequired(message=('Please enter a username'))])
    password = PasswordField('Password', [validators.DataRequired()])
    firstname = StringField('First Name', [validators.DataRequired(message=('Enter your first name'))])
    lastname = StringField('Last Name', [validators.DataRequired(message=('Enter your last name'))])
    email = StringField('Email', [validators.DataRequired(message=('Enter your email')),validators.Email(message=('Enter a valid email address'))])
    submit = SubmitField('Submit')
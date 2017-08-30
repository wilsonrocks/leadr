from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, TextAreaField, HiddenField
from wtforms.validators import Length, Email


class Login_Form(FlaskForm):
    username = StringField()
    password = PasswordField()

class New_Jot_Form(FlaskForm):
    text = TextAreaField('Jot',validators=[Length(1,140)])
    id = HiddenField("id")

class New_Password_Form(FlaskForm):
    new_password = PasswordField('New Password', validators=[Length(min=8)])
    id = HiddenField('id')

class Forgot_Password_Form(FlaskForm):
    email = StringField(validators=[Email(message="That doesn't look like a valid email address.")])

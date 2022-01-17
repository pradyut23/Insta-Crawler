from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class AnonymousForm(FlaskForm):
    userID   = StringField("UserId", validators = [DataRequired()])
    submit   = SubmitField("Open")

class LoginForm(FlaskForm):
    user     = StringField("Username", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    submit   = SubmitField("Login")
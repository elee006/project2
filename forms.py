from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

def Invalid_Credentials(form, field):
    username_entered = form.username.data
    password_entered = field.data
    #credentials invalid
    user_object = User.query.filter_by(username=username_entered).first()
    if user_object is None():
        raise ValidationError("Username or Password Incorrect")
    elif password_entered != user_object.password:
         raise ValidationError("Username or Password Incorrect")

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
class loginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Invalid_Credentials])
    submit = SubmitField("Login")
                               

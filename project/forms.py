from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, InputRequired, email, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8)])
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=150)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    address = StringField('Address', validators=[DataRequired(), Length(min=5, max=200)])
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=100)])
    state = StringField('State', validators=[DataRequired(), Length(min=2, max=100)])
    country = StringField('Country', validators=[DataRequired(), Length(min=2, max=100)])
    zip_code = StringField('Zip Code', validators=[DataRequired(), Length(4)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8)])
    submit = SubmitField('Login')

# form used in basket
class CheckoutForm(FlaskForm):
    firstname = StringField("Your first name", validators = [InputRequired()])
    surname = StringField("Your surname", validators = [InputRequired()])
    email = StringField("Your email", validators = [InputRequired(), email()])
    phone = StringField("Your phone number", validators = [InputRequired()])
    submit = SubmitField("Send to Agent")


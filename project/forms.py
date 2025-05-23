from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, InputRequired, email, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8)])
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
    address1 = StringField("Address line 1", validators = [InputRequired()])
    address2 = StringField("Address line 2")
    city = StringField("City", validators = [InputRequired()])
    state = StringField("State", validators = [InputRequired()])
    postcode = StringField("Postcode", validators = [InputRequired()])
    submit = SubmitField("Send to Agent")


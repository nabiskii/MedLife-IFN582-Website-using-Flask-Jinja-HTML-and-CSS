from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, InputRequired, email, EqualTo, NumberRange

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

# Admin manage form
# --- ITEM FORM ---
class AddItemForm(FlaskForm):
    itemCode = StringField('Item Code', validators=[DataRequired(), Length(max=10)])
    itemName = StringField('Item Name', validators=[DataRequired(), Length(max=100)])
    itemDescription = StringField('Item Description', validators=[DataRequired(), Length(max=250)])
    unitPrice = DecimalField('Unit Price', places=2, validators=[DataRequired(), NumberRange(min=0)])
    onhandQuantity = IntegerField('On-hand Quantity', validators=[DataRequired(), NumberRange(min=0)])

    supplierID = SelectField('Supplier', coerce=int, validators=[DataRequired()])
    categoryCode = SelectField('Category', validators=[DataRequired()])

    submit = SubmitField('Submit')

class EditItemForm(FlaskForm):
    itemCode = StringField('Item Code', render_kw={'readonly': True})  # read-only in form
    itemName = StringField('Item Name', validators=[DataRequired(), Length(max=100)])
    itemDescription = StringField('Item Description', validators=[DataRequired(), Length(max=250)])
    unitPrice = DecimalField('Unit Price', places=2, validators=[DataRequired(), NumberRange(min=0)])
    onhandQuantity = IntegerField('On-hand Quantity', validators=[DataRequired(), NumberRange(min=0)])

    supplierID = SelectField('Supplier', coerce=int, validators=[DataRequired()])
    categoryCode = SelectField('Category', validators=[DataRequired()])
    submit = SubmitField('Update Item')

# --- CATEGORY FORMS ---
class AddCategoryForm(FlaskForm):
    categoryCode = StringField('Category Code', validators=[DataRequired(), Length(max=2)])
    categoryName = StringField('Category Name', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Add Category')

class EditCategoryForm(FlaskForm):
    categoryName = StringField('Category Name', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Update Category')

# --- ORDER FORM ---
class AddOrderForm(FlaskForm):
    orderNo = IntegerField('Order Number', validators=[DataRequired(), NumberRange(min=0)])
    customerID = SelectField('Customer', coerce=int, validators=[DataRequired()])
    basketID = SelectField('Basket', coerce=int, validators=[DataRequired()])
    deliveryMethodCode = SelectField('Delivery Method', validators=[DataRequired()])
    submit = SubmitField('Create Order')

class EditOrderForm(FlaskForm):
    orderStatus = SelectField('Order Status', choices=[
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled')
    ], validators=[DataRequired()])
    submit = SubmitField('Update Order')

# --- USER FORMS ---
class AddUserForm(FlaskForm):
    userName = StringField('Username', validators=[DataRequired(), Length(max=20)])
    password = StringField('Password', validators=[DataRequired(), Length(max=80)])
    userType = SelectField('User Type', choices=[('Admin', 'Admin'), ('User', 'User')], validators=[DataRequired()])
    submit = SubmitField('Add User')

class EditUserForm(FlaskForm):
    userName = StringField('Username', validators=[DataRequired(), Length(max=20)])
    userType = SelectField('User Type', choices=[('Admin', 'Admin'), ('User', 'User')], validators=[DataRequired()])
    submit = SubmitField('Update User')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, IntegerField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, InputRequired, email, EqualTo, NumberRange

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=5)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=5)])
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
    state = SelectField("State", choices=[
        ('NSW', 'New South Wales'),
        ('VIC', 'Victoria'),
        ('QLD', 'Queensland'),
        ('WA', 'Western Australia'),
        ('SA', 'South Australia'),
        ('TAS', 'Tasmania'),
        ('ACT', 'Australian Capital Territory'),
        ('NT', 'Northern Territory')], validators = [InputRequired()])
    postcode = StringField("Postcode", validators = [InputRequired()])
    paymenttype = RadioField('Payment Type', choices=[
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('PayPal', 'PayPal')], validators=[InputRequired()])
    nameoncard = StringField('Name on Card', validators=[InputRequired(), Length(max=50)])
    cardnumber = StringField('Card Number', validators=[InputRequired(), Length(min=16, max=16)])
    expirydate = StringField('Expiry Date (MM/YY)', validators=[InputRequired(), Length(min=5, max=5)])
    cvv = PasswordField('CVV', validators=[InputRequired(), Length(min=3, max=3)], render_kw={'style':'margin-bottom: 15px;'})
    submit = SubmitField('Submit Payment')

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
    customerID = SelectField('Customer', coerce=int, validators=[DataRequired()])
    deliveryMethodCode = SelectField('Delivery Method', validators=[DataRequired()])
    orderTotalAmount = DecimalField('Order Total Amount', places=2, validators=[DataRequired()])
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

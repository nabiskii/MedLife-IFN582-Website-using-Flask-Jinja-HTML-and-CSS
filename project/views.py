from functools import wraps
from hashlib import sha256

from flask import *

from project.forms import CheckoutForm, LoginForm, RegisterForm
from .db import *
from .models import UserLogin
from .session import get_basket, convert_basket_to_order, empty_basket
from .wrapper import admin_required

bp = Blueprint('main', __name__)


# # Home page
# @bp.route('/')
# def index():
#     return render_template('index.html')

# User registration route
@bp.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = sha256(form.password.data.encode()).hexdigest()
        # Check if the user already exists
        user = check_for_user(form.username.data, form.password.data)
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE username = %s", [username])
        if cur.fetchone():
            flash('Username already exists.')
            return redirect(url_for('main.register'))
        cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                    (username, password, 'user'))
        mysql.connection.commit()
        cur.close()
        flash('Registration successful! Please login.')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

# User login route
@bp.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = check_for_user(form.username.data, sha256(form.password.data.encode()).hexdigest())
        if user != None:

            # Store full user info in session
            if user.userType == 'Admin':is_admin = True;
            else:is_admin = False;
            session['user'] = {
                'user_id': str(user.userID),
                'username': user.userName,
                'user_type': user.userType,
                'is_admin': is_admin,
            }
            session['logged_in'] = True
            flash('Login successful!')

            return redirect(url_for('main.index'))
        flash('Invalid username or password')
    return render_template('login.html', title='Log In', form=form)

# User logout route
@bp.route('/logout')
def logout():
    # logout_user()
    session.pop('user', None)
    session.pop('logged_in', None)
    flash('You have been logged out.')
    return redirect(url_for('main.login'))

# Dashboard for authenticated users
@bp.route('/manage/')
@admin_required
def manage():

    userAccount = UserLogin(int(session['user']['user_id']), session['user']['username'], None, session['user']['user_type'])

    return render_template('manage.html',  user=userAccount)

# Admin-only product management page
@bp.route('/manage/users')
@admin_required
def manage_users():
    accounts = get_all_users()

    return render_template('manage_users.html' ,accounts=accounts,)

@bp.route('/manage/add_user', methods=['GET', 'POST'])
@admin_required
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']

        # encrypt password
        encrypted_password = sha256(password.encode()).hexdigest()
        insert_user(username, encrypted_password, user_type)
        flash('User added successfully.', 'success')
        return redirect(url_for('main.manage'))
    return render_template('manage_add_user.html')

@bp.route('/manage/edit_user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('main.manage'))
    if request.method == 'POST':
        username = request.form['username']
        user_type = request.form['user_type']
        update_user(user_id, username, user_type)
        flash('User updated successfully.', 'success')
        return redirect(url_for('main.manage'))
    return render_template('manage_edit_user.html', user=user)

@bp.route('/manage/delete_user/<int:user_id>')
@admin_required
def delete_user(user_id):
    delete_from_user(user_id)
    flash('User deleted.', 'success')
    return redirect(url_for('main.manage'))

# Admin-only product management page
@bp.route('/manage/products')
@admin_required
def manage_products():
    return "Admin-only product management page."

# Admin-only category management page
@bp.route('/manage/categories')
@admin_required
def manage_categories():
    return "Admin-only category management page."

# Admin-only order management page
@bp.route('/manage/orders')
@admin_required
def manage_orders():
    return "Admin-only order management page."

# ***init page navigation***
@bp.route('/', endpoint='index')
def index():
    services = [
        {
            "title": "Prescription Medicine Delivery",
            "description": "Get your prescription medicines delivered quickly and securely, ensuring you never miss a dose."
        },
        {
            "title": "OTC Medication",
            "description": "Shop for a wide range of health and wellness products, including vitamins, supplements, and personal care items."
        },
        {
            "title": "Special delivery types",
            "description": "Choose from a variety of delivery options, including temperature-controlled delivery."
        },
        {
            "title": "24/7 Customer support",
            "description": "Our support team is here round the clock for your orders, queries, and health-related needs."
        }
    ]

    products = [
        {
            "name": "Panadol Rapid 48 Caplets",
            "price": "10.00",
            "image": "panadol.jpg"
        },
        {
            "name": "Nurofen Zavance 96 pack",
            "price": "15.00",
            "image": "ibuprofen.jpg"
        },
        {
            "name": "Claratyne Allergy & Hayfever Relief",
            "price": "9.50",
            "image": "antihistamine.jpg"
        },
        {
            "name": "CeraVe Moisturising Cream",
            "price": "25.99",
            "image": "cerave cream.jpg"
        },
        {
            "name": "CeraVe Skin Renewing Night Cream",
            "price": "36.99",
            "image": "cerave night cream.jpg"
        },
        {
            "name": "Maybelline Lasting Fix Setting Loose Powder",
            "price": "9.99",
            "image": "maybelline powder.jpg"
        },
        {
            "name": "Maybelline Fit Me True-to-tone Blush",
            "price": "9.50",
            "image": "maybelline blush.jpg"
        },
        {
            "name": "Difflam Plus Sore Throat Anaesthetic Spray",
            "price": "8.45",
            "image": "sore throat.jpg"
        }
    ]

    return render_template("index.html", services=services, products=products)

@bp.route("/checkout/", methods=["GET", "POST"] )
def checkout():
    form = CheckoutForm()
    if request.method == 'POST':

        # retrieve correct order object
        order = get_basket()

        if form.validate_on_submit():
            order.status = True
            order.firstname = form.firstname.data
            order.surname = form.surname.data
            order.email = form.email.data
            order.phone = form.phone.data
            flash('Thank you for your information, your order is being processed!', )
            order = convert_basket_to_order(get_basket())
            empty_basket()
            add_order(order)
            print('Number of orders in db: {}'.format(len(get_orders())))
            return redirect(url_for('main.index'))
        else:
            flash('The provided information is missing or incorrect',
                  'error')

    return render_template('checkout.html', form=form)

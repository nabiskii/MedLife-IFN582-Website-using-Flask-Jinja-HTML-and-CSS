from functools import wraps
from hashlib import sha256

from flask import *
from flask_login import UserMixin, current_user, login_user, login_required, logout_user
from . import mysql, login_manager
from werkzeug.security import check_password_hash, generate_password_hash

from project import mysql
from project.forms import CheckoutForm, LoginForm, RegisterForm
from .db import *
from .session import get_basket, convert_basket_to_order, empty_basket

bp = Blueprint('main', __name__)

# ***init session management***

# itemdetails/<int:item_id>
# /
# order/<int:item_id>
# order/<int:item_id>/<int:quantity>
# order/<int:item_id>/<int:quantity>/<string:action>(for updating the quantity)
# checkout/
# admin pages
# clear basket
# remove item from basket/<int:item_id>

class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

# Load user object from user ID (used by Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    user = get_user_by_id(user_id)
    return User(user.id, user.username, user.role) if user else None

# Decorator for admin-only routes
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            return "Access Denied: Admins only", 403
        return f(*args, **kwargs)
    return decorated_function

# User registration route
@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # Retrieve username and password from the form
            username = form.username.data
            password = sha256(form.password.data.encode()).hexdigest()

            # Check if the username already exists
            user = check_user_exists(username)
            if user:
                flash('Username already exists.')
                return redirect(url_for('main.register'))
            
            # If username does not exist, add the user into the database
            else:
                add_user(username, password)
                flash('Registration successful! Please login.')
                return redirect(url_for('main.login'))
        
    return render_template('register.html', form=form)

# User login route
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = sha256(form.password.data.encode()).hexdigest()
            # Check if the user exists in the database
            user = get_user_by_login(username, password)

            if not user:
                flash('Invalid username or password')
                return redirect(url_for('main.login'))
            
            session['user']={
                'user_id': user.id,
                'username': user.username,
                'role': user.role
            }
            session['logged_in'] = True
            session['is_admin'] = is_admin(username)
            flash('Login successful!')
            return redirect(url_for('main.dashboard') if session['is_admin'] else url_for('main.index'))
        
        return render_template('login.html', title='Log In', form=form)

# User logout route
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# Dashboard for authenticated users
@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

# Admin-only product management page
@bp.route('/admin/products')
@admin_required
def admin_products():
    return "Admin-only product management page."

# Admin-only category management page
@bp.route('/admin/categories')
@admin_required
def admin_categories():
    return "Admin-only category management page."

# Admin-only order management page
@bp.route('/admin/orders')
@admin_required
def admin_orders():
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

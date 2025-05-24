from functools import wraps
from hashlib import sha256
from subprocess import check_call

from flask import *
from flask_login import UserMixin, current_user, login_user, login_required, logout_user
from . import login_manager
from project.forms import CheckoutForm, LoginForm, RegisterForm
from .db import *
from .session import *

bp = Blueprint('main', __name__)

# ***init session management***

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

# manage for authenticated users
@bp.route('/manage')
def manage():
    return render_template('manage.html', user=current_user)

# ***init page navigation***
@bp.route('/', methods=['GET'])
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

    all_categories = get_all_categories()
    selected_category = request.args.get('category', 'all')
    search = request.args.get('search','').strip()
    print(search)

    if search:
        items = search_items(search)
    elif selected_category == 'all':
        items = get_items()
    else:
        items = get_items_by_category(selected_category)

    return render_template("index.html", services=services, items=items, all_categories=all_categories, search=search, selected_category=selected_category)

@bp.route('/product_details/<int:item_id>')
def product_details(item_id):
    return render_template('product_details.html', item=get_item(item_id))

@bp.route('/order/')
def order():
    basket = get_basket()

    return render_template('order.html', basket=basket, basket_total=basket.total_cost())

@bp.route('/order/<int:item_id>')
def order_add(item_id):
    basket = get_basket()
    item = get_item(item_id)
    
    if not item:
        flash('Item not found.')
        return redirect(url_for('main.index'))

    # Add to basket or increment quantity
    add_to_basket(item_id)
    
    print(get_basket(),"getting the basket")
    return redirect(url_for('main.order'))
    return render_template('order.html', item=item, basket=basket, basket_total=basket.total_cost())

@bp.route('/order/<int:item_id>/<int:quantity>')
def order_with_quantity(item_id, quantity):
    basket = get_basket()
    item = get_item(item_id)

    if not item:
        flash('Item not found.')
        return redirect(url_for('main.index'))

    add_to_basket(item_id, quantity)
    return render_template('order.html', item=item, basket=basket, basket_total=basket.total_cost())

@bp.route('/order/<int:item_id>/<string:action>', methods =['POST'])
def order_with_quantity_action(item_id, action):
    removing_itemid = False
    basket = get_basket()
    item = get_item(item_id)

    if not item:
        flash('Item not found.')
        return redirect(url_for('main.index'))

    for basket_item in basket.items:
        if basket_item.id == item_id:
            if action == 'increase':
                basket_item.increment_quantity()
            elif action == 'decrease':
                basket_item.decrement_quantity()
                if basket_item.quantity == 0:
                    removing_itemid = True
                    break
    
    if removing_itemid:
        remove_from_basket(item_id)
        flash(f'{item.name} removed from basket.')

    return render_template('order.html', item=item, basket=basket, basket_total=basket.total_cost())

@bp.route('/removeitem/<int:item_id>')
def remove_item(item_id):
    item = get_item(item_id)

    if not item:
        flash('Item not found.')
        return redirect(url_for('main.index'))

    # remove item from basket
    remove_from_basket(item_id)
    flash(f'{item.name} removed from basket.')
    return redirect(url_for('main.order', item_id=item_id))

@bp.route('/clearbasket/')
def clear_basket():
    # Clear the basket in the session
    empty_basket()
    flash('Basket cleared successfully.')
    return redirect(url_for('main.order'))

@bp.route("/checkout/", methods=["GET", "POST"] )
def checkout():
    form = CheckoutForm()
    check_basket = get_basket()
    if request.method == 'POST':
        # check if user is logged in
        if not session.get('logged_in'):
            flash('Please log in to proceed with checkout.', 'error')
            return redirect(url_for('main.login'))
        
        print(check_basket)
        # check if basket is empty
        if not check_basket:
            flash('Your basket is empty. Please add items to your basket before checking out.', 'error')
            return redirect(url_for('main.index'))

        if form.validate_on_submit():
            if not check_customer_exists(session['user']['user_id']):
                cust_id = add_customer(session['user']['user_id'], form.firstname.data, form.surname.data, form.email.data, form.phone.data, form.address1.data, form.address2.data, form.city.data, form.state.data, form.postcode.data)
            else:
                cust_id = get_customer_id(session['user']['user_id'])
            
            order = convert_basket_to_order(check_basket)
            order_id = add_order(order, cust_id)
            flash(f"Thank you, {session['user']['username']}! Your order #{order_id} has been placed successfully.",)
            empty_basket()
            return redirect(url_for('main.index'))
        else:
            flash('The provided information is missing or incorrect','error')

    return render_template('checkout.html', form=form, basket=check_basket, basket_total=check_basket.total_cost())

'''

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

'''

# User registration route
@bp.route('/register', methods=['POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        print("inside request method")
        if form.validate_on_submit():
            print("inside form validate")
            # Retrieve username and password from the form
            username = form.username.data
            password = sha256(form.password.data.encode()).hexdigest()

            # Check if the username already exists
            user = check_user_exists(username)
            print(user)
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
            return redirect(url_for('main.manage') if session['is_admin'] else url_for('main.index'))
        
    return render_template('login.html', title='Log In', form=form)

# User logout route
@bp.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('logged_in', None)
    session.pop('is_admin', None)
    flash('You have been logged out successfully!')
    return redirect(url_for('main.login'))
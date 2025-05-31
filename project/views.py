from hashlib import sha256

from flask import Blueprint, flash, redirect, url_for, render_template, request

from project.forms import *
from . import db, session
from . import models
from .session import get_basket, convert_basket_to_order, empty_basket, add_to_basket, remove_from_basket
from .wrapper import admin_required
from .models import DeliveryMethod, OrderStatus

bp = Blueprint('main', __name__)

# User registration route
@bp.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # Get the username and hashed password
            username = form.username.data
            password = sha256(form.password.data.encode()).hexdigest()
            # Check if the user already exists
            user= db.check_user_exists(username)
            if user:
                flash('Username already exists.', 'danger')
                return redirect(url_for('main.login'))
            
            # Add the user to the database
            db.add_user(username, password, 'User')
            flash('Registration successful! Please login.','success')
            return redirect(url_for('main.login'))
        
    return render_template('register.html', form=form)

# User login route
@bp.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():

            # Check if the user exists and password is correct
            user = db.check_for_user(form.username.data, sha256(form.password.data.encode()).hexdigest())
            if user is not None:

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
                flash('Login successful!','success')

                return redirect(url_for('main.index'))
            
            flash('Invalid username or password','danger')
    return render_template('login.html', title='Log In', form=form)

# User logout route
@bp.route('/logout')
def logout():
    # Logout user by clearing session data
    session.pop('user', None)
    session.pop('logged_in', None)
    flash('You have been logged out.','success')
    return redirect(url_for('main.index'))

# Dashboard for authenticated users
@bp.route('/manage/')
@admin_required
def manage():
    userAccount = models.UserLogin(int(session['user']['user_id']), session['user']['username'], "", session['user']['user_type'])
    return render_template('manage.html',  user=userAccount)

# Admin-only user management page
@bp.route('/manage/users')
@admin_required
def manage_users():
    accounts = db.get_all_users()

    return render_template('manage_users.html' ,accounts=accounts,)

# Admin-only page to add users.
@bp.route('/manage/add_user', methods=['GET', 'POST'])
@admin_required
def add_user():
    form = AddUserForm()
    if request.method == 'POST':
        username = form.userName.data
        password = form.password.data
        user_type = form.userType.data

        # encrypt password
        encrypted_password = sha256(password.encode()).hexdigest()
        db.insert_user(username, encrypted_password, user_type)
        flash('User added successfully.', 'success')
        return redirect(url_for('main.manage_users'))
    return render_template('manage_add_user.html',add_user_form=form)

# Admin-only page to edit users.
@bp.route('/manage/edit_user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = db.get_user_by_id(user_id)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('main.manage'))
    form=EditUserForm(data=user)
    if request.method == 'POST':
        username = form.userName.data
        user_type = form.userType.data
        db.update_user(user_id, username, user_type)
        flash('User updated successfully.', 'success')
        return redirect(url_for('main.manage_users'))
    return render_template('manage_edit_user.html', edit_user_form=form)

# Admin-only page to delete users.
@bp.route('/manage/delete_user/<int:user_id>')
@admin_required
def delete_user(user_id):
    user = db.get_user_by_id(user_id)
    username = user['userName']
    db.delete_from_user(user_id)
    flash(f'User {username} deleted.', 'success')
    return redirect(url_for('main.manage_users'))

# Admin-only item management page
@bp.route('/manage/items')
@admin_required
def manage_items():
    items = db.get_admin_all_items()
    return render_template('manage_items.html', items=items)

# Admin-only page to add items.
@bp.route('/add_item', methods=['GET', 'POST'])
@admin_required
def add_item():
    form = AddItemForm()
    # Populate supplier and category dropdowns from DB
    suppliers = db.get_all_suppliers()
    categories = db.get_all_categories()

    form.supplierID.choices = [(s['supplierID'], s['supplierName']) for s in suppliers]
    form.categoryCode.choices = [(c['categoryCode'], c['categoryName']) for c in categories]

    if form.validate_on_submit():
        db.add_item(
            form.itemCode.data,
            form.itemName.data,
            form.itemDescription.data,
            form.unitPrice.data,
            form.onhandQuantity.data,
            form.supplierID.data,
            form.categoryCode.data
        )
        flash('Item added successfully!', 'success')
        return redirect(url_for('main.manage_items'))
    return render_template('manage_add_item.html', item_form=form)

# Admin-only page to edit items.
@bp.route('/edit_item/<code>', methods=['GET', 'POST'])
@admin_required
def edit_item(code):
    item = db.get_item_by_code(code)
    if item is None:
        flash('Item not found.', 'danger')
        return redirect(url_for('main.manage_items'))

    form = EditItemForm(data=item)  # preload form with item values

    # Populate dropdown choices
    suppliers = db.get_all_suppliers()
    categories = db.get_all_categories()

    form.supplierID.choices = [(s['supplierID'], s['supplierName']) for s in suppliers]
    form.categoryCode.choices = [(c['categoryCode'], c['categoryName']) for c in categories]

    if form.validate_on_submit():
        db.update_item(
            code,
            form.itemName.data,
            form.itemDescription.data,
            form.unitPrice.data,
            form.onhandQuantity.data,
            form.supplierID.data,
            form.categoryCode.data
        )
        flash('Item updated successfully!', 'success')
        return redirect(url_for('main.manage_items'))

    return render_template('manage_edit_item.html', item_form=form, item=item)

# Admin-only page to delete items.
@bp.route('/delete_item/<code>')
@admin_required
def delete_item(code):
    db.delete_item(code)
    flash('Item deleted successfully.', 'success')
    return redirect(url_for('main.manage_items'))

# Admin-only category management page
@bp.route('/manage/categories')
@admin_required
def manage_categories():
    categories = db.get_all_categories()
    return render_template('manage_categories.html', categories=categories)

# Admin-only page to add categories.
@bp.route('/add_category', methods=['GET', 'POST'])
@admin_required
def add_category():
    form = AddCategoryForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            db.add_category(
                form.categoryCode.data,
                form.categoryName.data
            )
            flash('Category added!', 'success')
            return redirect(url_for('main.manage_categories'))
        else:
            flash('Category submission failed.', 'danger')
    return render_template('manage_add_category.html', add_category_form=form)

# Admin-only page to edit categories.
@bp.route('/edit_category/<code>', methods=['GET', 'POST'])
@admin_required
def edit_category(code):
    category = db.get_category_by_code(code)
    form = EditCategoryForm(categoryName=category['categoryName'])
    if form.validate_on_submit():
        db.update_category(code, form.categoryName.data)
        flash('Category updated!', 'success')
        return redirect(url_for('main.manage_categories'))
    return render_template('manage_edit_category.html', edit_category_form=form, code=code)

# Admin-only page to delete categories.
@bp.route('/delete_category/<code>')
@admin_required
def delete_category(code):
    items = db.get_items_by_category(code)

    #if there are items associated with the category, do not delete it.
    if items:
        flash("This category has items associated with it, please edit or delete the items before continuing.")
        return redirect(url_for('main.manage_categories'))
    else:
        db.delete_category(code)
        flash('Category deleted.', 'success')
        return redirect(url_for('main.manage_categories'))

# Admin-only order management page
@bp.route('/manage/orders')
@admin_required
def manage_orders():
    orders = db.get_all_orders()
    return render_template('manage_orders.html', orders=orders)

# Admin-only page to add orders.
@bp.route('/add_order', methods=['GET', 'POST'])
@admin_required
def add_order():
    form = AddOrderForm()

    # Populate dropdowns
    customers = db.get_all_customers()
    methods = db.get_all_delivery_methods()

    form.customerID.choices = [(c['customerID'], f"{c['firstName']} {c['surname']}") for c in customers]
    form.deliveryMethodCode.choices = [(m['deliveryMethodCode'], m['deliveryMethodName']) for m in methods]

    if form.validate_on_submit():
        db.add_order_admin(

            form.customerID.data,
            form.deliveryMethodCode.data,
            form.orderTotalAmount.data,
        )
        flash("Order successfully added!", "success")
        return redirect(url_for('main.manage_orders'))

    return render_template("manage_add_order.html", add_order_form=form)

# Admin-only page to edit orders.
@bp.route('/edit_order/<int:order_id>', methods=['GET', 'POST'])
@admin_required
def edit_order(order_id):
    order = db.get_order_by_id(order_id)
    form = EditOrderForm(obj=order)
    if form.validate_on_submit():
        db.update_order_status(order_id, form.orderStatus.data)
        flash('Order updated!', 'success')
        return redirect(url_for('main.manage_orders'))
    return render_template('manage_edit_order.html', edit_order_form=form, order=order, order_id=order_id)

# Admin-only page to delete orders.
@bp.route('/delete_order/<int:order_id>')
@admin_required
def delete_order(order_id):
    db.delete_order(order_id)
    flash('Order deleted.', 'success')
    return redirect(url_for('main.manage_orders'))


# index route for the main page
@bp.route('/', methods=['GET'])
def index():

    # Service offerings
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

    # Get all the categories and search if exists, and items based on the selected category or search term.
    all_categories = db.get_distinct_all_categories()
    selected_category = request.args.get('category', 'all')
    search = request.args.get('search','').strip()

    if search:
        items = db.search_items(search)
    elif selected_category == 'all':
        items = db.get_items()
    else:
        items = db.get_items_by_category(selected_category)

    return render_template("index.html", services=services, items=items, all_categories=all_categories, search=search, selected_category=selected_category)

# Product details route
@bp.route('/product_details/<int:item_id>')
def product_details(item_id):
    quantity = int(request.args.get('quantity',1))

    # Check if the quantity is a positive integer
    if quantity < 1:
        flash("Quantity must be more than zero.", "error")
        return redirect(url_for('main.product_details', item_id=item_id))
    return render_template('product_details.html', item=db.get_item(item_id))

# Basket page route
@bp.route('/order/', methods=['GET'])
def order():
    basket = get_basket()
    return render_template('order.html', basket=basket, basket_total=basket.total_cost())

# Basket add an item with quantity 1.
@bp.route('/order/<int:item_id>')
def order_add(item_id):
    item = db.get_item(item_id)
    
    if not item:
        flash('Item not found.')
        return redirect(url_for('main.index'))

    # Add to basket or increment quantity
    add_to_basket(item_id)
    
    return redirect(url_for('main.order'))

# Basket add an item with quantity.
@bp.route('/order/<int:item_id>/<int:quantity>')
def order_with_quantity(item_id, quantity):

    basket = get_basket()
    item = db.get_item(item_id)

    if not item:
        flash('Item not found.')
        return redirect(url_for('main.index'))

    add_to_basket(item_id, quantity)
    return redirect(url_for('main.order'))

# Basket action with quantity increase or decrease.
@bp.route('/order/<int:item_id>/<string:action>', methods =['POST'])
def order_with_quantity_action(item_id, action):
    tmp_basket = get_basket()
    item = db.get_item(item_id)

    # Check if item exists in the database and if it does, check action and update quantity.
    if not item:
        flash('Item not found.')
        return redirect(url_for('main.index'))


    for basket_item in tmp_basket.items:
        if basket_item.id == item_id:

            if action == 'increase':
                basket_item.increment_quantity()
                break
            elif action == 'decrease':
                if basket_item.quantity > 1:
                    basket_item.decrement_quantity()
                else:
                    remove_from_basket(item_id)
                break

    session['basket'] = tmp_basket
    return redirect(url_for('main.order'))

# Basket remove an item.
@bp.route('/removeitem/<int:item_id>')
def remove_item(item_id):
    item = db.get_item(item_id)

    if not item:
        flash('Item not found.')
        return redirect(url_for('main.index'))

    # remove item from basket
    remove_from_basket(item_id)
    flash(f'{item.itemName} removed from basket.')

    return redirect(url_for('main.order'))

# Basket clear all items.
@bp.route('/clearbasket/')
def clear_basket():
    # Clear the basket in the session
    empty_basket()
    flash('Basket cleared successfully.')
    return redirect(url_for('main.order'))

# Checkout route
@bp.route("/checkout/", methods=["GET", "POST"] )
def checkout():
    form = CheckoutForm()
    basket = get_basket()
    basket_total = basket.total_cost()
    basket_num_items = basket.get_total_quantity()

    if request.method == 'POST':
        # check if user is logged in
        if not session.get('logged_in'):
            flash('Please log in to proceed with checkout.', 'error')
            return redirect(url_for('main.login'))
        
        # check if basket is empty
        if not basket:
            flash('Your basket is empty. Please add items to your basket before checking out.', 'error')
            return redirect(url_for('main.index'))

        if form.validate_on_submit():
            delivery_price = request.form.get('delivery')
            if not delivery_price:
                flash('Please select a delivery method.', 'error')
                return redirect(url_for('main.checkout'))

            # Get the delivery method based on the price and calculate the final price
            delivery_method = db.get_delivery_method_by_price(delivery_price)

            final_price = basket_total + int(delivery_price)

            # Check if the customer exists, if not create a new customer and get the customer ID
            if not db.check_customer_exists(session['user']['user_id']):
                cust_id = db.add_customer(session['user']['user_id'], form)
            else:
                cust_id = db.get_customer_id(session['user']['user_id'])
            
            # Create the order object and add it to the database
            order = convert_basket_to_order(cust_id, delivery_method, final_price)
            order_id = db.add_order(order, "Confirmed")

            flash(f"Thank you, {session['user']['username']}! Your order #{order_id} has been placed successfully.",)
            empty_basket()
            return redirect(url_for('main.index'))
        else:
            flash('The provided information is missing or incorrect','error')
    return render_template('checkout.html', form=form, basket=basket, basket_total=basket_total, delivery_methods=DeliveryMethod, basket_num_items=basket_num_items)

# Subscription route
@bp.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    # Validate email
    if not email:
        flash('Email is required.', 'error')
        return redirect(url_for('main.index'))

    # Check if email is already subscribed else insert it.
    try:
        db.insert_subscription(email)
        flash('Thank you for subscribing!', 'success')
    except Exception as e:
        flash('Subscription failed: ' + str(e), 'error')
    return redirect(url_for('main.index'))

# Trigger Error handling route for 500 error.
@bp.route('/trigger_500')
def trigger_500():
    # Force a division by zero error
    return 1/0
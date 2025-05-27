from hashlib import sha256

from flask import Blueprint, flash, redirect, url_for, render_template, request

from project.forms import *
from . import db, session
from . import models
from .session import get_basket, convert_basket_to_order, empty_basket, add_to_basket, remove_from_basket
from .wrapper import admin_required
from .models import DeliveryMethod

bp = Blueprint('main', __name__)

# User registration route
@bp.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = sha256(form.password.data.encode()).hexdigest()
            # Check if the user already exists
            cur = db.mysql.connection.cursor()
            cur.execute("SELECT userID FROM users WHERE username = %s", [username])
            if cur.fetchone():
                flash('Username already exists.', 'danger')
                cur.close()
                return redirect(url_for('main.register'))
            cur.execute("INSERT INTO users (userName, password, userType) VALUES (%s, %s, %s)",
                        (username, password, 'User'))
            db.mysql.connection.commit()
            cur.close()
            flash('Registration successful! Please login.','success')
            return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

# User login route
@bp.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
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
    # logout_user()
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

@bp.route('/manage/add_user', methods=['GET', 'POST'])
@admin_required
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']

        # encrypt password
        encrypted_password = sha256(password.encode()).hexdigest()
        db.insert_user(username, encrypted_password, user_type)
        flash('User added successfully.', 'success')
        return redirect(url_for('main.manage_users'))
    return render_template('manage_add_user.html')

@bp.route('/manage/edit_user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = db.get_user_by_id(user_id)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('main.manage'))
    if request.method == 'POST':
        username = request.form['username']
        user_type = request.form['user_type']
        db.update_user(user_id, username, user_type)
        flash('User updated successfully.', 'success')
        return redirect(url_for('main.manage_users'))
    return render_template('manage_edit_user.html', user=user)

@bp.route('/manage/delete_user/<int:user_id>')
@admin_required
def delete_user(user_id):
    user = db.get_user_by_id(user_id)
    username = user['userName']
    db.delete_from_user(user_id)
    flash(f'User {username} deleted.', 'success')
    return redirect(url_for('main.manage_users'))

# Admin-only product management page
@bp.route('/manage/items')
@admin_required
def manage_items():
    items = db.get_admin_all_items()
    return render_template('manage_items.html', items=items)

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

@bp.route('/edit_item/<code>', methods=['GET', 'POST'])
@admin_required
def edit_item(code):
    print("editing item code value",code)
    item = db.get_item_by_code(code)
    print(item, "item in edit_item")
    if item is None:
        print(item, "item in edit_item not found")
        flash('Item not found.', 'danger')
        return redirect(url_for('main.manage_items'))

    print("crossed the item not found check")
    form = EditItemForm(data=item)  # preload form with item values

    # Populate dropdown choices
    suppliers = db.get_all_suppliers()
    categories = db.get_all_categories()

    form.supplierID.choices = [(s['supplierID'], s['supplierName']) for s in suppliers]
    form.categoryCode.choices = [(c['categoryCode'], c['categoryName']) for c in categories]

    # reassign
    form.supplierID.data = item['supplierID']
    form.categoryCode.data = item['categoryCode']

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


@bp.route('/delete_category/<code>')
@admin_required
def delete_category(code):
    db.delete_category(code)
    flash('Category deleted.', 'success')
    return redirect(url_for('main.manage_categories'))

# Admin-only order management page
@bp.route('/manage/orders')
@admin_required
def manage_orders():
    orders = db.get_all_orders()
    return render_template('manage_orders.html', orders=orders)

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

@bp.route('/delete_order/<int:order_id>')
@admin_required
def delete_order(order_id):
    db.delete_order(order_id)
    flash('Order deleted.', 'success')
    return redirect(url_for('main.manage_orders'))


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

    all_categories = db.get_distinct_all_categories()
    selected_category = request.args.get('category', 'all')
    search = request.args.get('search','').strip()
    print(search)

    if search:
        items = db.search_items(search)
    elif selected_category == 'all':
        items = db.get_items()
    else:
        items = db.get_items_by_category(selected_category)

    return render_template("index.html", services=services, items=items, all_categories=all_categories, search=search, selected_category=selected_category)

@bp.route('/product_details/<int:item_id>')
def product_details(item_id):
    return render_template('product_details.html', item=db.get_item(item_id))

@bp.route('/order/', methods=['GET'])
def order():
    print("inside order")
    basket = get_basket()

    return render_template('order.html', basket=basket, basket_total=basket.total_cost())

@bp.route('/order/<int:item_id>')
def order_add(item_id):
    item = db.get_item(item_id)
    
    if not item:
        flash('Item not found.')
        return redirect(url_for('main.index'))

    # Add to basket or increment quantity
    add_to_basket(item_id)
    
    print(get_basket(),"getting the basket")
    return redirect(url_for('main.order'))

@bp.route('/order/<int:item_id>/<int:quantity>')
def order_with_quantity(item_id, quantity):
    print("inside order with quantity")
    basket = get_basket()
    item = db.get_item(item_id)

    if not item:
        flash('Item not found.')
        return redirect(url_for('main.index'))

    add_to_basket(item_id, quantity)
    return redirect(url_for('main.order'))

@bp.route('/order/<int:item_id>/<string:action>', methods =['POST'])
def order_with_quantity_action(item_id, action):
    tmp_basket = get_basket()
    item = db.get_item(item_id)
    print("item in order_with_quantity_action: ", item)

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

@bp.route('/removeitem/<int:item_id>')
def remove_item(item_id):
    print("inside remove item")
    item = db.get_item(item_id)

    if not item:
        flash('Item not found.')
        return redirect(url_for('main.index'))

    # remove item from basket
    remove_from_basket(item_id)
    flash(f'{item.itemName} removed from basket.')

    return redirect(url_for('main.order'))


@bp.route('/clearbasket/')
def clear_basket():
    # Clear the basket in the session
    empty_basket()
    flash('Basket cleared successfully.')
    return redirect(url_for('main.order'))

@bp.route("/checkout/", methods=["GET", "POST"] )
def checkout():
    form = CheckoutForm()
    basket = get_basket()
    selected_method = int(request.args.get('delivery', 5))
    basket_total = basket.total_cost()+selected_method
    basket_num_items = basket.get_total_quantity()

    if request.method == 'POST':
        print("Checkout POST request received")
        # check if user is logged in
        if not session.get('logged_in'):
            flash('Please log in to proceed with checkout.', 'error')
            return redirect(url_for('main.login'))
        
        print("checkout basket data: ",basket)
        # check if basket is empty
        if not basket:
            flash('Your basket is empty. Please add items to your basket before checking out.', 'error')
            return redirect(url_for('main.index'))

        # get delivery method name
        delivery_method = models.DeliveryMethod.get_delivery_method_by_amount(selected_method)

        if form.validate_on_submit():
            if not db.check_customer_exists(session['user']['user_id']):
                cust_id = db.add_customer(session['user']['user_id'], form)
            else:
                cust_id = db.get_customer_id(session['user']['user_id'])
            
            order = convert_basket_to_order(cust_id, delivery_method, basket_total)
            order_id = db.add_order(order)

            flash(f"Thank you, {session['user']['username']}! Your order #{order_id} has been placed successfully.",)
            empty_basket()
            return redirect(url_for('main.index'))
        else:
            flash('The provided information is missing or incorrect','error')
    return render_template('checkout.html', form=form, basket=basket, basket_total=basket_total, delivery_methods=DeliveryMethod, selected_method=selected_method, basket_num_items=basket_num_items)

@bp.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    if not email:
        flash('Email is required.', 'error')
        return redirect(url_for('main.index'))

    try:
        db.insert_subscription(email)
        flash('Thank you for subscribing!', 'success')
    except Exception as e:
        flash('Subscription failed: ' + str(e), 'error')
    return redirect(url_for('main.index'))

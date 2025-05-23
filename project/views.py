from hashlib import sha256

from flask import *

from project.forms import *
from . import db
from . import models
from .session import get_basket, convert_basket_to_order, empty_basket
from .wrapper import admin_required

bp = Blueprint('main', __name__)

# User registration route
@bp.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = sha256(form.password.data.encode()).hexdigest()
        # Check if the user already exists
        cur = db.mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE username = %s", [username])
        if cur.fetchone():
            flash('Username already exists.', 'danger')
            return redirect(url_for('main.register'))
        cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                    (username, password, 'user'))
        db.mysql.connection.commit()
        cur.close()
        flash('Registration successful! Please login.','success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

# User login route
@bp.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
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
    return redirect(url_for('main.login'))

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
        return redirect(url_for('main.manage'))
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
        return redirect(url_for('main.manage'))
    return render_template('manage_edit_user.html', user=user)

@bp.route('/manage/delete_user/<int:user_id>')
@admin_required
def delete_user(user_id):
    db.delete_from_user(user_id)
    flash('User deleted.', 'success')
    return redirect(url_for('main.manage'))

# Admin-only product management page
@bp.route('/manage/items')
@admin_required
def manage_items():
    items = db.get_all_items()
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
    item = db.get_item_by_code(code)
    if not item:
        flash('Item not found.', 'danger')
        return redirect(url_for('main.manage_items'))

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
    if db.item_is_in_baskets(code):
        flash('Cannot delete item; it is added to user baskets.', 'danger')
        return redirect(url_for('main.manage_items'))

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
    baskets = db.get_all_baskets()
    methods = db.get_all_delivery_methods()

    form.customerID.choices = [(c['customerID'], f"{c['firstName']} {c['surname']}") for c in customers]
    form.basketID.choices = [(b['basketID'], f"Basket #{b['basketID']} (Customer {b['customerID']})") for b in baskets]
    form.deliveryMethodCode.choices = [(m['deliveryMethodCode'], m['deliveryMethodName']) for m in methods]

    if form.validate_on_submit():
        db.add_order_admin(
            form.orderNo.data,
            form.customerID.data,
            form.basketID.data,
            form.deliveryMethodCode.data
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
            db.add_order(order)
            print('Number of orders in db: {}'.format(len(db.get_orders())))
            return redirect(url_for('main.index'))
        else:
            flash('The provided information is missing or incorrect',
                  'error')

    return render_template('checkout.html', form=form)

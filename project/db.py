from project import mysql
from project.models import *


#  ----------- user query -------------
def check_for_user(username, hash_password):
    cur = mysql.connection.cursor()
    cur.execute("SELECT userID, userName, password, userType FROM users WHERE userName = %s AND password = %s",
                (username, hash_password))
    row = cur.fetchone()
    cur.close()
    if row:
        return UserLogin(row['userID'], row['userName'], row['password'], row['userType'])
    return None


def is_admin(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE userType = 'Admin' AND userID = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    if user and user['userType'] == 'admin':
        return True
    return False


def get_user_by_id(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT userID, userName, userType FROM users WHERE userID = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    return user


def get_all_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT userID, userName, userType FROM users")
    users = cur.fetchall()
    cur.close()
    return users


def insert_user(username, password, user_type):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (userName, password, userType) VALUES (%s, %s, %s)",
                (username, password, user_type))
    mysql.connection.commit()
    cur.close()


def update_user(user_id, username, user_type):
    user_type = user_type.strip()  # Clean whitespace
    if user_type not in ('Admin', 'User'):
        raise ValueError(f"Invalid userType: {user_type}")

    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET userName = %s, userType = %s WHERE userID = %s",
                (username, user_type, user_id))
    mysql.connection.commit()
    cur.close()


def delete_from_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE userID = %s", (user_id,))
    mysql.connection.commit()
    cur.close()


#  ----------- item query -------------
def get_all_items():
    cur = mysql.connection.cursor()
    cur.execute("SELECT itemCode, itemName AS name, itemDescription, unitPrice AS price, imageURL AS image FROM items")
    items = cur.fetchall()
    cur.close()
    return items


def get_admin_all_items():
    cur = mysql.connection.cursor()
    cur.execute("SELECT itemCode, itemName, unitPrice, onhandQuantity FROM items")
    items = cur.fetchall()
    cur.close()
    return items



def get_item_by_code(code):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM items WHERE itemCode = %s", (code,))
    item = cur.fetchone()
    cur.close()
    return item


def add_item(code, name, desc, price, quantity, supplierID, categoryCode):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO items (itemCode, itemName, itemDescription, unitPrice, onhandQuantity, supplierID, categoryCode, imageURL) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (code, name, desc, price, quantity, supplierID, categoryCode, 'no-img.jpg'))
    mysql.connection.commit()
    cur.close()


def update_item(code, name, description, price, quantity, supplierID, categoryCode):
    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE items SET itemName = %s, itemDescription = %s, unitPrice = %s, onhandQuantity = %s, supplierID = %s, categoryCode = %s WHERE itemCode = %s",
        (name, description, price, quantity, supplierID, categoryCode, code))
    mysql.connection.commit()
    cur.close()


def delete_item(code):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM items WHERE itemCode = %s", (code,))
    mysql.connection.commit()
    cur.close()


#  ----------- category query -------------
def get_all_categories():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM category")
    categories = cur.fetchall()
    cur.close()
    return categories


def get_category_by_code(code):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM category WHERE categoryCode = %s", (code,))
    category = cur.fetchone()
    cur.close()
    return category


def add_category(code, name):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO category (categoryCode, categoryName) VALUES (%s, %s)", (code, name))
    mysql.connection.commit()
    cur.close()


def update_category(code, name):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE category SET categoryName = %s WHERE categoryCode = %s", (name, code))
    mysql.connection.commit()
    cur.close()


def delete_category(code):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM category WHERE categoryCode = %s", (code,))
    mysql.connection.commit()
    cur.close()


#  ----------- order query -------------
def get_all_orders():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM orders")
    orders = cur.fetchall()
    cur.close()
    return orders


def get_order_by_id(order_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM orders WHERE orderID = %s", (order_id,))
    order = cur.fetchone()
    cur.close()
    return order


def add_order_admin(customerID, deliveryMethodCode, orderTotalAmount):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO orders (customerID, deliveryMethodCode, orderTotalAmount) VALUES (%s, %s, %s)",
                (customerID, deliveryMethodCode, orderTotalAmount))
    mysql.connection.commit()
    cur.close()


def update_order_status(order_id, status):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE orders SET orderStatus = %s WHERE orderID = %s", (status, order_id))
    mysql.connection.commit()
    cur.close()


def delete_order(order_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM orders WHERE orderID = %s", (order_id,))
    mysql.connection.commit()
    cur.close()


#  ----------- supplier query -------------
def get_all_suppliers():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM suppliers")
    suppliers = cur.fetchall()
    cur.close()
    return suppliers


#  ----------- customers query -------------
def get_all_customers():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM customers")
    customers = cur.fetchall()
    cur.close()
    return customers


#  ----------- delivery method query -------------
def get_all_delivery_methods():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM delivery_methods")
    methods = cur.fetchall()
    cur.close()
    return methods


#  ----------- subscription query -------------
def insert_subscription(email):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO subscription (emailAddress) VALUES (%s)", (email,))
    mysql.connection.commit()
    cur.close()



def add_user(username, password):
    """Add a new user."""
    cur = mysql.connection.cursor()
    cur.execute("""
                INSERT INTO users (userName, password, userType)
                VALUES (%s, %s, %s)
                """, (username,
                      password,
                      "User"))
    mysql.connection.commit()
    cur.close()


def get_user_by_login(username, password):
    """Get a user by username."""
    cur = mysql.connection.cursor()
    cur.execute("SELECT userID, userName, password, userType FROM users WHERE userName = %s AND password = %s",
                (username, password))
    user = cur.fetchone()
    cur.close()
    if user:
        return UserAccount(
            id=user['userID'],
            username=user['userName'],
            password=user['password'],
            role=user['userType']
        )
    return None



def check_user_exists(username):
    """Check if a user exists by username."""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE userName = %s", (username,))
    user = cur.fetchone()
    cur.close()
    return user is not None


def check_customer_exists(userID):
    """Check if a customer exists by userID."""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM customers WHERE userID = %s", (userID,))
    customer = cur.fetchone()
    cur.close()
    return customer is not None


def add_customer(form):
    """Add a new customer."""
    cur = mysql.connection.cursor()
    cur.execute("""
                INSERT INTO customers (firstName, surname, phoneNumber, emailAddress, addressLine1, addressLine2, city, state, postCode)
                VALUES (%s, %s, %s)
                """, (form.firstname.data,
                      form.surname.data,
                      form.phone.data,
                      form.email.data,
                      form.address1.data,
                      form.address2.data,
                      form.city.data,
                      form.state.data,
                      form.postcode.data))

    cust_id = cur.lastrowid
    mysql.connection.commit()
    cur.close()
    return cust_id


def get_customer_id(userID):
    """Get a customer ID by userID."""
    cur = mysql.connection.cursor()
    cur.execute("SELECT customerID FROM customers WHERE userID = %s", (userID,))
    customer = cur.fetchone()
    cur.close()
    if customer:
        return customer['customerID']
    return None


# item CRUD
def get_items():
    """Get all items."""
    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT items.itemCode AS 'Item Code',
                items.itemName AS 'Item Name',
                items.itemDescription AS 'Item Description',
                items.itemLongDescription1 AS 'Instruction',
                items.itemLongDescription2 AS 'Ingredients',
                items.unitPrice AS 'Unit Price',
                category.categoryName AS 'Category Name',
                suppliers.supplierName AS 'Supplier Name',
                items.onhandQuantity AS 'Onhand Quantity',
                items.imageURL AS 'Image'
            FROM items
            LEFT JOIN 
                category ON category.categoryCode = items.categoryCode
            LEFT JOIN 
                suppliers ON suppliers.supplierID = items.supplierID
            ORDER BY
                items.itemName;
                """)
    items = cur.fetchall()
    cur.close()
    return [Item(str(item['Item Code']),
                 item['Item Name'],
                 item['Item Description'],
                 item['Instruction'],
                 item['Ingredients'],
                 item['Unit Price'],
                 item['Category Name'],
                 item['Supplier Name'],
                 item['Onhand Quantity'],
                 item['Image']) for item in items]


def get_item(item_id):
    """Get a particular item based on item id."""
    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT items.itemCode AS 'Item Code',
                    items.itemName AS 'Item Name',
                    items.itemDescription AS 'Item Description',
                    items.itemLongDescription1 AS 'Instruction',
                    items.itemLongDescription2 AS 'Ingredients',
                    items.unitPrice AS 'Unit Price',
                    category.categoryName AS 'Category Name',
                    suppliers.supplierName AS 'Supplier Name',
                    items.onhandQuantity AS 'Onhand Quantity',
                    items.imageURL AS 'Image'
                FROM 
                    items
                LEFT JOIN 
                    category ON category.categoryCode = items.categoryCode
                LEFT JOIN 
                    suppliers ON suppliers.supplierID = items.supplierID
                WHERE 
                    items.itemCode = %s
                ORDER BY 
                    items.itemName;
                """, (item_id,))
    item = cur.fetchone()
    cur.close()
    return Item(str(item['Item Code']),
                item['Item Name'],
                item['Item Description'],
                item['Instruction'],
                item['Ingredients'],
                item['Unit Price'],
                item['Category Name'],
                item['Supplier Name'],
                item['Onhand Quantity'],
                item['Image'])


def get_items_by_category(category):
    """Get items by category."""
    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT items.itemCode AS 'Item Code',
                items.itemName AS 'Item Name',
                items.itemDescription AS 'Item Description',
                items.itemLongDescription1 AS 'Instruction',
                items.itemLongDescription2 AS 'Ingredients',
                items.unitPrice AS 'Unit Price',
                category.categoryName AS 'Category Name',
                suppliers.supplierName AS 'Supplier Name',
                items.onhandQuantity AS 'Onhand Quantity',
                items.imageURL AS 'Image'
            FROM items
            LEFT JOIN 
                category ON category.categoryCode = items.categoryCode
            LEFT JOIN 
                suppliers ON suppliers.supplierID = items.supplierID
            WHERE category.categoryCode = %s
            ORDER BY
                items.itemName;
                """, (category,))
    items = cur.fetchall()
    cur.close()
    return [Item(str(item['Item Code']),
                 item['Item Name'],
                 item['Item Description'],
                 item['Instruction'],
                 item['Ingredients'],
                 item['Unit Price'],
                 item['Category Name'],
                 item['Supplier Name'],
                 item['Onhand Quantity'],
                 item['Image']) for item in items]


def search_items(search):
    """Search for items by name."""
    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT items.itemCode AS 'Item Code',
                items.itemName AS 'Item Name',
                items.itemDescription AS 'Item Description',
                items.itemLongDescription1 AS 'Instruction',
                items.itemLongDescription2 AS 'Ingredients',
                items.unitPrice AS 'Unit Price',
                category.categoryName AS 'Category Name',
                suppliers.supplierName AS 'Supplier Name',
                items.onhandQuantity AS 'Onhand Quantity',
                items.imageURL AS 'Image'
            FROM items
            LEFT JOIN 
                category ON category.categoryCode = items.categoryCode
            LEFT JOIN 
                suppliers ON suppliers.supplierID = items.supplierID
            WHERE items.itemName LIKE %s OR items.itemDescription LIKE %s
            OR items.itemLongDescription1 LIKE %s OR items.itemLongDescription2 LIKE %s
            ORDER BY
                items.itemName;
                """, ('%' + search + '%', '%' + search + '%', '%' + search + '%', '%' + search + '%'))
    items = cur.fetchall()
    cur.close()
    return [Item(str(item['Item Code']),
                 item['Item Name'],
                 item['Item Description'],
                 item['Instruction'],
                 item['Ingredients'],
                 item['Unit Price'],
                 item['Category Name'],
                 item['Supplier Name'],
                 item['Onhand Quantity'],
                 item['Image']) for item in items]




#  ----------- category query -------------
def get_distinct_all_categories():
    cur = mysql.connection.cursor()
    cur.execute("SELECT DISTINCT * FROM category")
    categories = cur.fetchall()
    cur.close()
    return [Category(
        code=categories['categoryCode'],
        name=categories['categoryName']) for categories in categories]


#  Orders CRUD
def add_order(order, customer_id):
    """Add a new order."""
    cur = mysql.connection.cursor()
    cur.execute("""
                INSERT INTO orders (orderID, customerID, deliveryCode, totalCost, orderDate)
                VALUES (%s, %s, %s, %s)
                """, (order.id,
                      customer_id,
                      order.deliverycode,
                      order.total_cost,
                      datetime.now()))

    order_id = cur.lastrowid
    mysql.connection.commit()
    cur.close()
    return order_id

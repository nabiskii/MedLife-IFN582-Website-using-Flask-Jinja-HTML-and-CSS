
from datetime import datetime
from . import mysql
from project.models import *

# User CRUD
def is_admin(username):
    """Check if a user is an admin."""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE userName = %s", (username,))
    user = cur.fetchone()
    cur.close()
    if user and user[3] == 'admin':
        return True
    return False

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
    cur.execute("SELECT userID, userName, password, userType FROM users WHERE userName = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()
    if user:
        return UserAccount(
            id = user[0],
            username=user[1],
            password=user[2],
            role=user[3]
        )
    return None

def get_user_by_id(user_id):
    """Get a user by ID."""
    cur = mysql.connection.cursor()
    cur.execute("SELECT userID, userName, password, userType FROM users WHERE userID = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    if user:
        return UserAccount(
            id=user[0],
            username=user[1],
            password=user[2],
            role=user[3]
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

def add_cutomer(form):
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
    mysql.connection.commit()
    cur.close()


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
                items.imagePath AS 'Image'
            FROM items
            LEFT JOIN 
                (category, suppliers) ON (category.categoryCode = items.categoryCode
                AND suppliers.supplierID = items.supplierID)
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
                items.imagePath AS 'Image'
            FROM items
            WHERE items.itemCode = %s
            LEFT JOIN 
                (category, suppliers) ON (category.categoryCode = items.categoryCode
                AND suppliers.supplierID = items.supplierID)
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

def add_item(item):
    """Add a new item."""
    cur = mysql.connection.cursor()
    cur.execute("""
                INSERT INTO items (itemCode, itemName, itemDescription,
                itemLongDescription1, itemLongDescription2, unitPrice,
                categoryCode, supplierID, onhandQuantity, imagePath)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (item.id,
                      item.name,
                      item.description,
                      item.instruction,
                      item.ingredients,
                      item.price,
                      item.category,
                      item.supplier,
                      item.onhand_quantity,
                      item.image))
    mysql.connection.commit()
    cur.close()

# admin manage item
def update_item(item_id, udt_item):
    """Update a item by its ID."""
    item_id = str(item_id)
    for id in range(0, len(Item)):
        if Item[id].code == item_id:
            Item[id] = udt_item

def remove_item(item_id):
        """Remove a item by its ID."""
        for id in range(0, len(Item)):
            if Item[id].code == item_id:
                Item.pop(id)

#  Orders CRUD
def get_orders():
    """Get all orders."""
    return Orders

def get_order(order_id):
    """Get an order by its ID."""
    order_id = str(order_id)
    for order in Orders:
        if order.id == order_id:
            return order
    return None  # or raise an exception if preferred

def add_order(order):
    """Add a new order."""
    Orders.append(order)

def update_order(order_id, udt_order):
    """Update a order by its ID."""
    order_id = str(order_id)
    for id in range(0, len(Orders)):
        if Orders[id].id == order_id:
            Orders[id] = udt_order

def remove_order(order_id):
        """Remove a order by its ID."""
        for id in range(0, len(Orders)):
            if Orders[id].id == order_id:
                Orders.pop(id)



from datetime import datetime

from project import mysql
from project.models import *

DummyProduct = Product('1', 'Claratyne Allergy & Hayfever Relief',
         'This is description for Claratyne Allergy & Hayfever Relief',79,
        'p_pic1.jpg', 9.50, datetime(2023, 7, 23), 4.9)

Products = [
    Product('1', 'Claratyne Allergy & Hayfever Relief',
         'This is description for Claratyne Allergy & Hayfever Relief',79,
        'p_pic1.jpg', 9.50, datetime(2023, 7, 23), 4.9),
    Product('2', 'Nurofen Zavance 96 pack',
         'This is description for Nurofen Zavance 96 pack',100,
         'p_pic2.jpg', 15.00,  datetime(2023, 10, 30),4.8),
    Product('3', 'Panadol Rapid 48 Caplets',
         'This is description for Panadol Rapid 48 Caplets', 310,
         'p_pic3.jpg', 10.00,  datetime(2023, 10, 30),3.8)
]

DummyUserInfo = UserInfo(
    '0', 'Dummy', 'Foobar', 'dummy@foobar.com', '1234567890'
)

Orders = [
    Order('1', OrderStatus.PENDING, DummyUserInfo, 149.99,
          []),
    Order('2', OrderStatus.CONFIRMED, DummyUserInfo, 1000.00,
          [])
]

# User Info
def get_user():
    return DummyUserInfo

def get_all_user():
    return DummyUserInfo

def is_admin(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE userType = 'Admin' AND userID = %i", (user_id,))
    row = cur.fetchone()
    cur.close()
    return True if row else False

# Product CRUD
def get_products():
    """Get all products."""
    return Products

def get_product(product_id):
    """Get a product by its ID."""
    product_id = str(product_id)
    for product in Products:
        if product.id == product_id:
            return product
    return DummyProduct

def add_product(product):
    """Add a new product."""
    Products.append(product)

def update_product(product_id, udt_product):
    """Update a product by its ID."""
    product_id = str(product_id)
    for id in range(0, len(Products)):
        if Products[id].id == product_id:
            Products[id] = udt_product

def remove_product(product_id):
        """Remove a product by its ID."""
        for id in range(0, len(Products)):
            if Products[id].id == product_id:
                Products.pop(id)

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


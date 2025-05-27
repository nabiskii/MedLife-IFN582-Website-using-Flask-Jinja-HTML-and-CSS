from flask import session

from project.models import *
from project.db import get_item

DummyBasket = Basket()

def get_basket():
    basket_data = session.get('basket', {})
    print("session basket data:", basket_data)
    basket = Basket()
    print("Basket Data from Session:", basket_data)
    if not basket_data:
        return basket
    else:
        for item_data in basket_data.get('items', []):
            item_id = item_data['id']
            item = get_item(item_id)
            quantity = item_data['quantity']

            if item:
                basket.add_item(BasketItem(item_id, item, quantity))
    return basket

def _save_basket_to_session(basket):
    session['basket'] = {
        'items': [
            {
                'id': item.id,
                'item': get_item(item.id),
                'quantity': item.quantity
            } for item in basket.items
        ]
    }
    session.modified = True

def add_to_basket(item_id, quantity=1):
    basket = get_basket()
    existing_item = False
    for item in basket.items:
        if item.id == item_id:
            item.quantity += quantity
            existing_item = True
            _save_basket_to_session(basket)
            break
    if not existing_item:
        # If the item is not already in the basket, add it
        basket.add_item(BasketItem(item_id, get_item(item_id), quantity))
    # now store/update the basket in the session
    _save_basket_to_session(basket)

def remove_from_basket(item_id):
    basket = get_basket()
    basket.remove_item(item_id)
    # now store/update the basket in the session
    _save_basket_to_session(basket)

def empty_basket():
    session['basket'] = {"items": []}

def convert_basket_to_order(cust_id, delivery_method, total_cost):
    # convert the basket to an order
    order = Order(
        customerID = cust_id,
        deliveryMethodCode = delivery_method,
        orderTotalAmount= total_cost
    )
    return order
from flask import session

from project.models import *
from project.db import get_item

DummyBasket = Basket()


def get_basket():
    basket_data = session.get('basket', {})
    basket = Basket()
    print("Basket Data from Session:", basket_data)
    if not basket_data:
        return basket
    else:
        for item_data in basket_data.get('items', []):
            item_id = item_data['id']
            quantity = item_data['quantity']
            item = get_item(item_id)

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
    existing_item = next((i for i in basket.items if i.id == item_id), None)
    if existing_item:
        existing_item.increment_quantity()
    else:
        basket.add_item(BasketItem(item_id, get_item(item_id), quantity))
    # now store/update the basket in the session
    _save_basket_to_session(basket)

def remove_from_basket(basket_item_id):
    basket = get_basket()
    basket.remove_item(basket_item_id)
    # now store/update the basket in the session
    _save_basket_to_session(basket)

def empty_basket():
    session['basket'] = DummyBasket
    _save_basket_to_session(DummyBasket)

def convert_basket_to_order(basket):
    # convert the basket to an order
    order = Order(
        orderID = int,
        deliveryMethodCode = DeliveryMethod.STANDARD,
        orderTotalAmount= basket.total_cost(),
        items = basket.items,
    )
    return order
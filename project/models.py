from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List


@dataclass
class OrderStatus(Enum):
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    CANCELLED = 'Cancelled'

    def is_pending(self):
        return self == OrderStatus.PENDING

    def is_confirmed(self):
        return self == OrderStatus.CONFIRMED

    def is_cancelled(self):
        return self == OrderStatus.CANCELLED


@dataclass
class DeliveryMethod(Enum):
    STANDARD = 5
    EXPRESS = 8
    ECO = 15
    TEMP = 25

    def get_delivery_method_by_amount(amount: float):
        for method in DeliveryMethod:
            if method.value == amount:
                return method.name

# --- Dataclasses (Models) ---
@dataclass
class Item:
    itemCode: str
    itemName: str
    itemDescription: str
    itemLongDescription1: str
    itemLongDescription2: str
    unitPrice: float
    discountPrice: float
    supplierID: int
    categoryName: str
    onhandQuantity: int
    imageURL: str = field(default='medicine sample.jpg')


@dataclass
class Category:
    categoryCode: str
    categoryName: str


@dataclass
class Order:
    customerID: int
    deliveryMethodCode: DeliveryMethod
    orderTotalAmount: float
    orderDate: datetime = field(
        default_factory=lambda: datetime.now(),
        init=True)

@dataclass
class CustomerInfo:
    id: str
    firstname: str
    surname: str
    phone: str
    email: str
    address1: str
    address2: str
    city: str
    state: str
    postcode: str


@dataclass
class Supplier:
    id: int
    name: str


@dataclass
class Category:
    code: str
    name: str


@dataclass
class UserLogin:
    userID: int
    userName: str
    password: str
    userType: str


@dataclass
class BasketItem:
    id: str
    item: Item
    quantity: int = 1

    def total_price(self):
        """Calculate the total price for this basket item."""
        if self.item.discountPrice:
            return self.item.discountPrice * self.quantity
        else:
            return self.item.unitPrice * self.quantity

    def increment_quantity(self):
        """Increment the quantity of this basket item."""
        self.quantity += 1

    def decrement_quantity(self):
        """Decrement the quantity of this basket item."""
        if self.quantity > 1:
            self.quantity -= 1


@dataclass
class Basket:
    items: List[BasketItem] = field(default_factory=lambda: [])

    def __len__(self):
        """Get the number of items in the basket."""
        return len(self.items)
    
    def get_total_quantity(self):
        """Get the total quantity of items in the basket."""
        return sum(item.quantity for item in self.items)

    def add_item(self, item: BasketItem):
        """Add an item to the basket."""
        self.items.append(item)

    def remove_item(self, item_id:str):
        """Remove an item from the basket by its ID."""
        self.items = [basketItem for basketItem in self.items if basketItem.id != item_id]

    def get_item(self, item_id: str):
        """Get a item from the basket by its ID."""
        for item in self.items:
            if item.id == item_id:
                return item
        return None
    
    #not used (remove)
    def empty(self):
        """Empty the basket."""
        self.items = []

    def total_cost(self):
        """Calculate the total cost of the basket."""
        return sum(item.total_price() for item in self.items)

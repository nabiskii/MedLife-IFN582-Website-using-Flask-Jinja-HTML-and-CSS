from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List


@dataclass
class Product:
    id: str
    name: str
    description: str
    reviews: int
    image: str = 'foobar.png'
    price: float = 10.00
    date: datetime = field(
        default_factory=lambda: datetime.now()
    )
    rating: float = 1.0


class OrderStatus(Enum):
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    CANCELLED = 'Cancelled'

@dataclass
class UserLogin:
    userID: int
    userName: str
    password: str
    userType: str

@dataclass
class UserInfo:
    id: str
    firstname: str
    surname: str
    email: str
    phone: str

@dataclass
class BasketItem:
    id: str
    product: Product
    quantity: int = 1

    def total_price(self):
        """Calculate the total price for this basket item."""
        return self.product.price * self.quantity

    def increment_quantity(self):
        """Increment the quantity of this basket item."""
        self.quantity += 1

    def decrement_quantity(self):
        """Decrement the quantity of this basket item."""
        if self.quantity > 1:
            self.quantity -= 1

@dataclass
class Basket:
    items: List[BasketItem] = field(
        default_factory=lambda: [])

    def add_item(self, item: BasketItem):
        """Add a tour to the basket."""
        self.items.append(item)

    def remove_item(self, item: BasketItem):
        """Remove a tour from the basket by its ID."""
        self.items = [tour for tour in self.items if tour.id != item.id]

    def get_item(self, item_id: str):
        """Get a tour from the basket by its ID."""
        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def empty(self):
        """Empty the basket."""
        self.items = []

    def total_cost(self):
        """Calculate the total cost of the basket."""
        return sum(item.total_price() for item in self.items)


@dataclass
class Order:
    id: str
    status: OrderStatus
    user: UserInfo
    total_cost: float = 0.0
    items: List[BasketItem] = field(
        default_factory=list,
        init=True)
    date: datetime = field(
        default_factory=lambda: datetime.now(),
        init=True)

from datetime import datetime

class Item:
    def __init__(self, item_id: int, name: str, size: int, price: float):
        self.item_id = item_id
        self.name = name
        self.size = size
        self.price = price


class ItemOrdered:
    def __init__(self, item: Item, quantity: int):
        self.item = item
        self.quantity = quantity

    def total_price(self) -> float:
        return self.item.price * self.quantity

class Order:
    def __init__(self, order_id: int, shop: int, order_date: datetime, items: list[ItemOrdered]):
        self.order_id = order_id
        self.shop = shop
        self.order_date = order_date
        self.items = items

    
    def total_price(self) -> float:
        return sum(item.total_price() for item in self.items)


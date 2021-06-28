from models.order_item import OrderItem
from common.database import db
from dataclasses import dataclass, asdict
from typing import List


@dataclass
class Order(db.Model):
    id: int
    order_items: List[OrderItem]
    address: str
    customer_name: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_items = db.relationship('OrderItem', backref='order', lazy=True)
    address = db.Column(db.String(100), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)


    def get_dict(self):
        return asdict(self)


    def __str__(self) -> str:
        return f'Order: id={self.id}, order_items={self.order_items}, address={self.address}, customer_name={self.customer_name}'

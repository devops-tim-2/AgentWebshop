from common.database import db
from dataclasses import dataclass, asdict


@dataclass
class OrderItem(db.Model):
    id: int
    product_id: int
    quantity: int
    total: int
    order_id: int

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)


    def get_dict(self):
        return asdict(self)


    def __str__(self) -> str:
        return f'Order item: id={self.id}, product_id={self.product_id}, quantity={self.quantity}, total={self.total}, order_id={self.order_id}'

from typing import List
from models.product import Product
from common.database import db
from dataclasses import dataclass, asdict


@dataclass
class Catalog(db.Model):
    id: int
    user_id: int
    products: List[Product]

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    products = db.relationship('Product', backref='catalog', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def get_dict(self):
        return asdict(self)


    def __str__(self) -> str:
        return f'Catalog: id={self.id}, products={self.products}, user_id={self.user_id}'

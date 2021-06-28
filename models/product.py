from common.database import db
from dataclasses import dataclass, asdict


@dataclass
class Product(db.Model):
    id: int
    name: str
    price: int
    quantity: int
    available: int
    image_url: str
    catalog_id: int

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    catalog_id = db.Column(db.Integer, db.ForeignKey('catalog.id'), nullable=False)


    def get_dict(self):
        return asdict(self)


    def __str__(self) -> str:
        return f'Product: id={self.id}, name={self.name}, price={self.price}, quantity={self.quantity}, available={self.available}, image_url={self.image_url}, catalog_id={self.image_url}'

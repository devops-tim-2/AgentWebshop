from typing import List
from dataclasses import dataclass, asdict

from sqlalchemy import Column, Integer, String, Boolean, \
     ForeignKey

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Model = declarative_base(name='Model')


@dataclass
class OrderItem(Model):
    __tablename__ = 'orderitem'
    id: int
    product_id: int
    quantity: int
    total: int
    order_id: int

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)


    def get_dict(self):
        return asdict(self)


    def __str__(self) -> str:
        return f'Order item: id={self.id}, product_id={self.product_id}, quantity={self.quantity}, total={self.total}, order_id={self.order_id}'

@dataclass
class Order(Model):
    __tablename__ = 'order'
    id: int
    order_items: List[OrderItem]
    address: str
    customer_name: str

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_items = relationship('OrderItem', backref='order', lazy=True)
    address = Column(String(100), nullable=False)
    customer_name = Column(String(100), nullable=False)


    def get_dict(self):
        return asdict(self)


    def __str__(self) -> str:
        return f'Order: id={self.id}, order_items={self.order_items}, address={self.address}, customer_name={self.customer_name}'

@dataclass
class Product(Model):
    __tablename__ = 'product'
    id: int
    name: str
    price: int
    quantity: int
    available: int
    image_url: str
    catalog_id: int

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    available = Column(Integer, nullable=False)
    image_url = Column(String(200), nullable=False)
    catalog_id = Column(Integer, ForeignKey('catalog.id'), nullable=False)


    def get_dict(self):
        return asdict(self)


    def __str__(self) -> str:
        return f'Product: id={self.id}, name={self.name}, price={self.price}, quantity={self.quantity}, available={self.available}, image_url={self.image_url}, catalog_id={self.image_url}'


@dataclass
class Catalog(Model):
    __tablename__ = 'catalog'
    id: int
    user_id: int
    products: List[Product]

    id = Column(Integer, primary_key=True, autoincrement=True)
    products = relationship('Product', backref='catalog', lazy=True)
    user_id = Column(Integer, ForeignKey('userprofile.id', ondelete='CASCADE'), nullable=False)


    def get_dict(self):
        return asdict(self)


    def __str__(self) -> str:
        return f'Catalog: id={self.id}, products={self.products}, user_id={self.user_id}'

@dataclass
class Report:
    product: Product
    info: str
    

    def get_dict(self):
        return asdict(self)

@dataclass
class User(Model):
    __tablename__ = 'userprofile'
    id: int
    username: str
    password: str
    catalog_id: int

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    catalog_id = Column(Integer, ForeignKey('catalog.id', ondelete='CASCADE'))


    def get_dict(self):
        return asdict(self)


    def __str__(self) -> str:
        return f'User: id={self.id}, username={self.username}, password={self.password}, catalog_id={self.catalog_id}'

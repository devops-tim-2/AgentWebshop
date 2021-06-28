from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from models.product import Product
from typing import List, Tuple
from common.database import db


def get_all() -> List[Product]:
    return Product.query.all()


def get(product_id: int) -> Product:
    return Product.query.get(product_id)


def create(product: Product) -> Product:
    db.session.add(product)
    db.session.commit()

    return product


def update(product: dict) -> Product:
    current_product = get(product['id'])

    if 'name' in product.keys():
        current_product.name = product['name']
    if 'price' in product.keys():
        current_product.price = product['price']
    if 'quantity' in product.keys():
        current_product.quantity = product['quantity']
    if 'available' in product.keys():
        current_product.available = product['available']
    if 'image_url' in product.keys():
        current_product.image_url = product['image_url']

    try:
        db.session.commit()

        return current_product
    except Exception:
        db.session.rollback()

        return None    


def delete(product_id: int) -> Tuple[str, bool]:
    try:
        db.session.delete(Product.query.get(product_id))
        db.session.commit()
    except UnmappedInstanceError:
        return f"Product with id {product_id} not found.", False
    except IntegrityError:
        return "It's not possible to delete the product for which there is an order.", False

    return "The product was successfully deleted.", True

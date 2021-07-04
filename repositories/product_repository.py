from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from models.models import Product
from typing import List, Tuple
from common.database import db_session, engine


def get_all() -> List[Product]:
    return Product.query.all()


def get(product_id: int) -> Product:
    return Product.query.get(product_id)


def create(product: Product) -> Product:
    db_session.add(product)
    db_session.commit()

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
        db_session.commit()

        return current_product
    except Exception:
        db_session.rollback()

        return None    


def delete(product_id: int) -> Tuple[str, bool]:
    try:
        product = Product.query.filter(Product.id == product_id).first()
        db_session.delete(product)
        db_session.commit()
    except UnmappedInstanceError:
        return f"Product with id {product_id} not found.", False
    except IntegrityError:
        return "It's not possible to delete the product for which there is an order.", False

    return "The product was successfully deleted.", True


def get_highest_revenue_product() -> dict:
    sql = text('SELECT product_id, sum(total) AS revenue FROM orderitem GROUP BY product_id ORDER BY revenue DESC;')
    result = engine.execute(sql).first()

    return {'product': get(result[0]), 'revenue': result[1]}


def get_best_selling_product() -> dict:
    sql = text('SELECT id, quantity-available AS sold FROM product ORDER BY sold DESC;')
    result = engine.execute(sql).first()

    return {'product': get(result[0]), 'sold': result[1]}

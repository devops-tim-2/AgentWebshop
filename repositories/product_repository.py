from sqlalchemy import text
from models.product import Product
from common.database import db


def get(product_id: int) -> Product:
    return Product.query.get(product_id)


def get_highest_revenue_product() -> dict:
    sql = text('SELECT product_id, sum(total) AS revenue FROM order_item GROUP BY product_id ORDER BY revenue DESC;')
    result = db.engine.execute(sql).first()

    return {'product': get(result[0]), 'revenue': result[1]}


def get_best_selling_product() -> dict:
    sql = text('SELECT id, quantity-available AS sold FROM product ORDER BY sold DESC;')
    result = db.engine.execute(sql).first()

    return {'product': get(result[0]), 'sold': result[1]}
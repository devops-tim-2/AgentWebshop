from models.product import Product
from models.catalog import Catalog
from models.user import User
from repositories import product_repository
from common.utils import check


def get_all():
    result, code = [product.get_dict() for product in product_repository.get_all()], 200
    return result, code


def get(product_id: int):
    if not product_id:
        return 'Product id is None', 400

    product = product_repository.get(product_id)
    result, code = (product.get_dict(), 200) if product else (product, 404)
    
    return result, code


def create(data: dict, user: dict):
    if check(data):
        return 'Some of the values are None, empty value or non-positive value', 400

    product = Product(**data, available=data['quantity'], catalog_id=user['catalog_id'])
    product = product_repository.create(product)

    result, code = product.get_dict(), 201

    return result, code

def update(data: dict, user: dict):
    if check(data):
        return 'Some of the values are None, empty value or non-positive value', 400

    product, code = get(data['id'])
    if not product:
        return product, code
    
    catalog = Catalog.query.get(product.catalog_id)
    owner = User.query.get(catalog.user_id)

    if user['id'] != owner.id:
        return 'This product is not your.', 400

    product = product_repository.update(data)

    result, code = (product.get_dict(), 200) if product else (product, 400)

    return result, code


def delete(product_id: int, user: dict):
    product, code = get(product_id)
    if not product:
        return product, code
    
    catalog = Catalog.query.get(product.catalog_id)
    owner = User.query.get(catalog.user_id)

    if user['id'] != owner.id:
        return 'This product is not your.', 400

    message, success = product_repository.delete(product_id)
    result = success

    if 'not found' in message:
        code = 404
    elif 'not possible' in message:
        code = 400
    else:
        code = 200

    return result, code

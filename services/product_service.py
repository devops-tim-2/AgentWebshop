from models.report import Report
from models.product import Product
from repositories import product_repository
from services import catalog_service, user_service
from common.utils import check
import json


def get_all():
    result, code = {'data': [product.get_dict() for product in product_repository.get_all()]}, 200
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
    
    catalog = catalog_service.get(product['catalog_id'])
    owner = user_service.get(catalog.user_id)

    if user['id'] != owner.id:
        return 'This product is not your.', 400

    product = product_repository.update(data)

    result, code = (product.get_dict(), 200) if product else (product, 400)

    return result, code


def delete(product_id: int, user: dict):
    product, code = get(product_id)
    if not product:
        return f"Product with id {product_id} not found.", 404
    
    catalog = catalog_service.get(product['catalog_id'])
    owner = user_service.get(catalog.user_id)

    if user['id'] != owner.id:
        return 'This product is not your.', 400

    message, success = product_repository.delete(product_id)
    
    return (message, 200) if success else (message, 400)


def highest_revenue_product() -> dict:
    product_info = product_repository.get_highest_revenue_product()
    result, code = Report(product_info['product'], '${} was earned on the product.'.format(product_info['revenue'])).get_dict(), 200

    return result, code


def best_selling_product() -> dict:
    product_info = product_repository.get_best_selling_product()
    result, code = Report(product_info['product'], '{} units of the product have been sold.'.format(product_info['sold'])).get_dict(), 200

    return result, code

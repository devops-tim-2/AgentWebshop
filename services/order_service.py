from models.models import Order, OrderItem
from repositories import order_repository, product_repository
from services import product_service
from common.utils import check


def get_all():
    result, code = {'data': [order.get_dict() for order in order_repository.get_all()]}, 200
    return result, code


def get(order_id: int):
    if not order_id:
        return 'Order id is None', 400

    order = order_repository.get(order_id)
    result, code = (order.get_dict(), 200) if order else (order, 404)
    
    return result, code


def create(data: dict):
    if check(data):
        return 'Some of the values are None, empty value or non-positive value', 400

    products = [] # da se ne dobavljaju dva puta proizvodi
    for item in data['order_items']:
        try:
            product, code = product_service.get(item['product_id'])
        except Exception:
            return f'Product not found.', 404
        
        if product is None:
            return f'Product with id {item["product_id"]} not found.', 404
        
        if item['quantity'] > product['available']:
            return f'There are no {item["quantity"]} units of the {product["name"]} product.', 400
        
        products.append(product)

    order_items = []
    for index, item in enumerate(data['order_items']):
        product = products[index]
        order_items.append(OrderItem(product_id=item['product_id'], quantity=item['quantity'], total=product['price']*item['quantity']))
        product['available'] -= item['quantity']

    order = Order(order_items=order_items, address=data['address'], customer_name=data['customer_name'])
    order = order_repository.create(order)

    for product in products:
        product_repository.update(product)

    result, code = order.get_dict(), 201

    return result, code

from models.order_item import OrderItem
from models.order import Order
from models.product import Product
from services import order_service


def test_create_ok(mocker):
    order_data = {
        "order_items": [
            {
                "quantity": 10,
                "product_id": 1
            }
        ],
        "address": "neka tamo adresa",
        "customer_name": "neko tamo ime"
    }

    product_data = {
        "name": "wiskey",
        "price": 10,
        "quantity": 1000,
        "image_url": "http://slika.jpg"
    }

    expected = Order(order_items=[OrderItem(product_id=1, quantity=1)], address=order_data['address'], customer_name=order_data['customer_name'])
    product_result = (Product(**product_data, available=product_data['quantity'], catalog_id=1), 200)

    mocker.patch('services.order_service.order_repository.create', return_value=expected)
    mocker.patch('services.order_service.product_service.get', return_value=product_result)

    actual, code = order_service.create(order_data)
    
    assert expected.get_dict()==actual
    assert product_result[0].available == product_result[0].quantity-order_data['order_items'][0]['quantity']


def test_create_not_enough_units(mocker):
    order_data = {
        "order_items": [
            {
                "quantity": 1001,
                "product_id": 1
            }
        ],
        "address": "neka tamo adresa",
        "customer_name": "neko tamo ime"
    }

    product_data = {
        "name": "wiskey",
        "price": 10,
        "quantity": 1000,
        "image_url": "http://slika.jpg"
    }

    expected = ('There are no {} units of the {} product.'.format(order_data['order_items'][0]['quantity'], product_data['name']), 400)
    product_result = (Product(**product_data, available=product_data['quantity'], catalog_id=1), 200)

    mocker.patch('services.order_service.product_service.get', return_value=product_result)

    actual = order_service.create(order_data)
    
    assert expected==actual

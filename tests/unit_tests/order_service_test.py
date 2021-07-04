from models.models import OrderItem, Order, Product, Catalog, User
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
        "id": 1,
        "name": "wiskey",
        "price": 10,
        "quantity": 1000,
        "available": 1000,
        "image_url": "http://slika.jpg"
    }

    expected = Order(order_items=[OrderItem(product_id=1, quantity=1)], address=order_data['address'], customer_name=order_data['customer_name'])
    product = Product(**product_data, catalog_id=1)

    mocker.patch('services.order_service.order_repository.create', return_value=expected)
    mocker.patch('services.order_service.product_service.get', return_value=(product_data, 200))
    mocker.patch('services.order_service.product_service.product_repository.get', return_value=product)

    actual, code = order_service.create(order_data)
    
    assert expected.get_dict()==actual


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
        "available": 1000,
        "image_url": "http://slika.jpg"
    }

    expected = (f'There are no {order_data["order_items"][0]["quantity"]} units of the {product_data["name"]} product.', 400)
    
    mocker.patch('services.order_service.order_repository.create', return_value=expected)
    mocker.patch('services.order_service.product_service.get', return_value=(product_data, 200))

    actual = order_service.create(order_data)
    
    assert expected==actual

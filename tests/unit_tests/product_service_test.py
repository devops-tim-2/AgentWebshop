from models.models import OrderItem, Order, Product, Catalog, User
from services import product_service


def test_create_ok(mocker):
    data = {
        "name": "wiskey",
        "price": 10,
        "quantity": 1000,
        "image_url": "http://slika.jpg"
    }

    user = {
        'username': 'admin',
        'password': 'admin',
        'catalog_id': 1
    }

    expected = Product(**data, available=data['quantity'], catalog_id=1)
    user = {'username': 'admin', 'password': 'admin', 'catalog_id': 1}

    mocker.patch('services.product_service.product_repository.create', return_value=expected)

    actual, code = product_service.create(data, user)

    assert expected.get_dict()==actual


def test_create_empty_value():
    data = {
        "name": "",
        "price": 10,
        "quantity": 1000,
        "image_url": "http://slika.jpg"
    }

    user = {
        'username': 'admin',
        'password': 'admin',
        'catalog_id': 1
    }

    expected = 'Some of the values are None, empty value or non-positive value', 400

    actual = product_service.create(data, user)

    assert expected==actual


def test_update_ok(mocker):
    product_data = {
        "id": 1,
        "name": "beerx3",
        "price": 30,
        "image_url": "http://slika3.jpg"
    }

    product = Product(**product_data)

    user_data = {
        'id': 1,
        'username': 'admin',
        'password': 'admin',
        'catalog_id': 1
    }

    user = User(**user_data)

    catalog_data = {
        'id': 1,
        'user_id': user_data['id']
    }



    mocker.patch('services.product_service.product_repository.get', return_value=product)
    mocker.patch('services.product_service.catalog_service.get', return_value=catalog_data)
    mocker.patch('services.product_service.user_service.get', return_value=user)
    mocker.patch('services.product_service.product_repository.update', return_value=product)

    actual, code = product_service.update(product_data, user_data)

    assert product.get_dict()==actual


def test_update_empty_value():
    data = {
        "id": 1,
        "name": "",
        "price": 30,
        "image_url": "http://slika3.jpg"
    }

    user = {
        'username': 'admin',
        'password': 'admin',
        'catalog_id': 1
    }

    expected = 'Some of the values are None, empty value or non-positive value', 400

    actual = product_service.update(data, user)

    assert expected==actual


def test_delete_ok(mocker):
    product_id = 1

    product_data = {
        "id": product_id,
        "name": "beerx3",
        "price": 30,
        "image_url": "http://slika3.jpg"
    }

    product = Product(**product_data)

    user_data = {
        'id': 1,
        'username': 'admin',
        'password': 'admin',
        'catalog_id': 1
    }

    user = User(**user_data)

    catalog_data = {
        'id': 1,
        'user_id': user_data['id']
    }


    message, code = "The product was successfully deleted.", 200

    mocker.patch('services.product_service.product_repository.get', return_value=product)
    mocker.patch('services.product_service.catalog_service.get', return_value=catalog_data)
    mocker.patch('services.product_service.user_service.get', return_value=user)
    mocker.patch('services.product_service.product_repository.delete', return_value=(message, code))

    actual_message, actual_code = product_service.delete(product_id, user_data)
    
    assert (message, code)==(actual_message, actual_code)


from models.user import User
from common.result import Result
from models.product import Product
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
    data = {
        "id": 1,
        "name": "beerx3",
        "price": 30,
        "image_url": "http://slika3.jpg"
    }

    expected = Product(**data)

    mocker.patch('services.product_service.product_repository.update', return_value=expected)

    actual, code = product_service.update(data)

    assert expected.get_dict()==actual


def test_update_empty_value():
    data = {
        "id": 1,
        "name": "",
        "price": 30,
        "image_url": "http://slika3.jpg"
    }

    expected = 'Some of the values are None, empty value or non-positive value', 400

    actual = product_service.update(data)

    assert expected==actual


def test_delete_ok(mocker):
    product_id = 1

    message, success = "The product was successfully deleted.", True

    mocker.patch('services.product_service.product_repository.delete', return_value=(message, success))

    actual = product_service.delete(product_id)
    
    assert success==actual


def test_delete_not_found(mocker):
    product_id = -1

    message, success = "Product with id {} not found.".format(product_id), False

    mocker.patch('services.product_service.product_repository.delete', return_value=(message, success))

    actual = product_service.delete(product_id)
    
    assert (message, success)==actual

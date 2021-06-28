from flask import Blueprint, request
from services import product_service
from common.utils import auth

product_api = Blueprint('product_api', __name__)


@product_api.route('', methods=["GET"])
def get_all():
    return product_service.get_all()

@product_api.route('/<int:product_id>', methods=["GET"])
def get(product_id: int):
    return product_service.get(product_id)


@product_api.route('', methods=["POST"])
def create():
    result, code = auth(request.headers)
    if code != 200:
        return result, code

    data = request.get_json()
    return product_service.create(data, result)


@product_api.route('', methods=["PUT"])
def update():
    result, code = auth(request.headers)
    if code != 200:
        return result, code

    data = request.get_json()
    return product_service.update(data, result)


@product_api.route('/<int:product_id>', methods=["DELETE"])
def delete(product_id: int):
    result, code = auth(request.headers)
    if code != 200:
        return result, code

    return product_service.delete(product_id, result)

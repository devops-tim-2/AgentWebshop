from common.utils import auth
from flask import Blueprint, request
from services import order_service

order_api = Blueprint('order_api', __name__)


@order_api.route('', methods=["GET"])
def get_all():
    result, code = auth(request.headers)
    if code != 200:
        return result, code

    return order_service.get_all()


@order_api.route('/<int:order_id>', methods=["GET"])
def get(order_id: int):
    result, code = auth(request.headers)
    if code != 200:
        return result, code

    return order_service.get(order_id)


@order_api.route('', methods=["POST"])
def create():
    data = request.get_json()
    return order_service.create(data)

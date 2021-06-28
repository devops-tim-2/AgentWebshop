from common.utils import auth
from flask import Blueprint, request
from services import order_service

order_api = Blueprint('order_api', __name__)


@order_api.route('', methods=["GET"])
def get_all():
    auth_result = auth(request.headers)
    if auth_result['code'] != 200:
        return auth_result

    return order_service.get_all()


@order_api.route('/<int:order_id>', methods=["GET"])
def get(order_id: int):
    auth_result = auth(request.headers)
    if auth_result['code'] != 200:
        return auth_result

    return order_service.get(order_id)


@order_api.route('', methods=["POST"])
def create():
    data = request.get_json()
    return order_service.create(data)

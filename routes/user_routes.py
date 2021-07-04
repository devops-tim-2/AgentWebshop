from flask import Blueprint, request
from services import user_service

user_api = Blueprint('user_api', __name__)


@user_api.route('/auth', methods=["POST"])
def login():
    data = request.get_json()
    return user_service.login(data)
    
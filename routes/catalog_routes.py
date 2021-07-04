from flask import Blueprint, request
from services import catalog_service
from common.utils import auth

catalog_api = Blueprint('caatalog_api', __name__)


@catalog_api.route('/<int:catalog_id>', methods=["GET"])
def get(catalog_id: int):
    return catalog_service.get(catalog_id)
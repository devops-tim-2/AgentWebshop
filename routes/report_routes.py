from common.utils import auth
from flask import Blueprint, request
from services import product_service

report_api = Blueprint('report_api', __name__)


@report_api.route('/highest-revenue-product', methods=["GET"])
def highest_revenue_product():
    result, code = auth(request.headers)
    if code != 200:
        return result, code

    return product_service.highest_revenue_product()


@report_api.route('/best-selling-product', methods=["GET"])
def best_selling_product():
    result, code = auth(request.headers)
    if code != 200:
        return result, code

    return product_service.best_selling_product()

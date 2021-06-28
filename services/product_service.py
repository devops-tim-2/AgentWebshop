from models.report import Report
from repositories import product_repository


def highest_revenue_product() -> dict:
    product_info = product_repository.get_highest_revenue_product()
    result, code = Report(product_info['product'], '${} was earned on the product.'.format(product_info['revenue'])).get_dict(), 200

    return result, code


def best_selling_product() -> dict:
    product_info = product_repository.get_best_selling_product()
    result, code = Report(product_info['product'], '{} units of the product have been sold.'.format(product_info['sold'])).get_dict(), 200

    return result, code

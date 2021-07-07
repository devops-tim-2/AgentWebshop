from repositories import catalog_repository, product_repository, user_repository


def get(catalog_id: int):
    catalog = catalog_repository.get(catalog_id).get_dict()
    catalog['products'] = [i.get_dict() for i in product_repository.get_from_catalog(catalog_id)]
    catalog['owner'] = user_repository.get_username(catalog_id).username
    return catalog

def create(user_id):
    return catalog_repository.create(user_id)
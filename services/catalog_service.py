from repositories import catalog_repository


def get(catalog_id: int):
    return catalog_repository.get(catalog_id)

def create(user_id):
    return catalog_repository.create(user_id)
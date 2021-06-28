from models.catalog import Catalog


def get(catalog_id: int) -> Catalog:
    return Catalog.query.filter_by(id=catalog_id).first()
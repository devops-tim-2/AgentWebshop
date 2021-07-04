from models.models import Catalog

from common.database import db_session


def get(catalog_id: int) -> Catalog:
    return Catalog.query.filter_by(id=catalog_id).first()

def create(user_id):
    catalog = Catalog(user_id=user_id)
    db_session.add(catalog)
    db_session.commit()
from models.models import User


def get(user_id: int) -> User:
    return User.query.filter_by(id=user_id).first()


def get_by_username(username: str) -> User:
    return User.query.filter_by(username=username).first()

def get_username(catalog_id):
    return User.query.filter(User.catalog_id == catalog_id).first()
from models.user import User


def get_by_username(username: str) -> User:
    return User.query.filter_by(username=username).first()

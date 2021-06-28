from models.user import User


def get(user_id: int) -> User:
    return User.query.filter_by(id=user_id).first()


def get_by_username(username: str) -> User:
    return User.query.filter_by(username=username).first()

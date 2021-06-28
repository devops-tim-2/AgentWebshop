from models.order import Order
from typing import List
from common.database import db


def get_all() -> List[Order]:
    return Order.query.all()


def get(order_id: int) -> Order:
    return Order.query.get(order_id)


def create(order: Order) -> Order:
    db.session.add(order)
    # db.session.commit()

    return order

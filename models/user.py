from common.database import db
from dataclasses import dataclass, asdict


@dataclass
class User(db.Model):
    id: int
    username: str
    password: str
    catalog_id: int

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    catalog_id = db.Column(db.Integer, db.ForeignKey('catalog.id'))


    def get_dict(self):
        return asdict(self)


    def __str__(self) -> str:
        return f'User: id={self.id}, username={self.username}, password={self.password}, catalog_id={self.catalog_id}'

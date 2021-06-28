from models.product import Product
from dataclasses import dataclass


@dataclass
class Report:
    product: Product
    info: str

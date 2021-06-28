from models.product import Product
from dataclasses import dataclass, asdict


@dataclass
class Report:
    product: Product
    info: str
    

    def get_dict(self):
        return asdict(self)

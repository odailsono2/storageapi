from __future__ import annotations
from dataclasses import dataclass
from .enums import ProductsCategory
from typing import NewType

ProductID = NewType("ProductID", int)


@dataclass(frozen=True)
class Product:
    id: ProductID
    name: str
    description: str
    price: float
    category: ProductsCategory
    stock: int
    active: bool = True

    @property
    def is_in_stock(self) -> bool:
        return self.stock > 0

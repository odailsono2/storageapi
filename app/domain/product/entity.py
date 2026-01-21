from __future__ import annotations
from dataclasses import dataclass
from typing import NewType

from .enums import ProductsCategory


ProductId = NewType("ProductId", int)


@dataclass(frozen=True)
class Product:
    id: ProductId
    name: str
    description: str
    price: float
    category: ProductsCategory
    stock: int
    active: bool = True

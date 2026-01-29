from __future__ import annotations
from dataclasses import dataclass

from app.domain.product.Shares import ProductId

from .enums import ProductsCategory


@dataclass(frozen=True)
class Product:
    id: ProductId
    name: str
    description: str
    price: float
    category: ProductsCategory
    stock: int
    active: bool = True

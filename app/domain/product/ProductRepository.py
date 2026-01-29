from __future__ import annotations

from typing import Protocol

from .entity import Product
from .Shares import ProductId
from .enums import ProductsCategory


class ProductRepository(Protocol):
    """Interface para o repositório de produtos."""

    def add(
        self,
        *,
        name: str,
        price: float,
        stock: int,
        category: ProductsCategory,
        description: str = "",
        active: bool = True,
    ) -> Product:
        """Adiciona um novo produto ao repositório."""
        ...

    def get_by_id(self, product_id: ProductId) -> Product | None:
        """Obtém um produto pelo seu ID."""
        ...

    def list(
        self,
        *,
        category: ProductsCategory | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        active: bool | None = None,
        min_stock: int | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Product]:
        """Lista produtos com base em filtros opcionais."""
        ...

    def update(self, product: Product) -> Product:
        """Atualiza um produto existente no repositório."""
        ...

    def delete(self, product_id: ProductId) -> None:
        """Remove um produto do repositório pelo seu ID."""
        ...

    def deativate(self, product_id: ProductId) -> Product:
        """Desativa um produto pelo seu ID."""
        ...

from __future__ import annotations

from dataclasses import replace
from typing import Iterable

from ...domain.product.Shares import ProductId

from ...domain.product.entity import Product
from ...domain.product.enums import ProductsCategory


class ProductRepository:
    """Interface para o repositório de produtos."""

    def __init__(self, repo: ProductRepository | None = None) -> None:
        self._products = {}
        self._next_id = 1

    def _new_id(self) -> ProductId:
        pid = ProductId(self._next_id)
        self._next_id += 1
        return pid

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
        product = Product(
            id=self._new_id(),
            name=name,
            price=price,
            stock=stock,
            description=description,
            category=category,
            active=active,
        )
        self._products[product.id] = product

        return product

    def get_by_id(self, product_id: ProductId) -> Product | None:
        """Obtém um produto pelo seu ID."""
        return self._products.get(product_id)

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
        items: Iterable[Product] = self._products.values()

        if category is not None:
            items = (p for p in items if p.category == category)
        if min_price is not None:
            items = (p for p in items if p.price >= min_price)
        if max_price is not None:
            items = (p for p in items if p.price <= max_price)
        if active is not None:
            items = (p for p in items if p.active == active)
        if min_stock is not None:
            items = (p for p in items if p.stock >= min_stock)

        # Ordenação previsível por ID
        sorted_items = sorted(items, key=lambda p: int(p.id))

        # Paginação defensiva
        if offset < 0:
            offset = 0
        if limit < 1:
            limit = 1

        return sorted_items[offset : offset + limit]

    def update_stock(self, product_id: ProductId, *, delta: int) -> Product:
        """
        Ajusta estoque (delta pode ser + ou -).
        Garante que estoque final não fique negativo.
        """
        current = self.require(product_id)

        new_stock = current.stock + delta
        if new_stock < 0:
            raise ValueError("Estoque insuficiente para a operação solicitada.")

        updated = replace(current, stock=new_stock)
        self._products[product_id] = updated
        return updated

    def delete(self, product_id: ProductId) -> None:
        """Remove um produto do repositório pelo seu ID."""
        self.require(product_id)
        del self._products[product_id]

    def require(self, product_id: ProductId) -> Product:
        """Obtém um produto pelo seu ID, ou levanta erro se não existir."""
        product = self.get_by_id(product_id)
        if product is None:
            raise KeyError(f"Produto com ID {product_id} não encontrado.")
        return product

    def change_active_status(self, product_id: ProductId, *, active: bool) -> Product:
        """Ativa ou desativa um produto."""
        current = self.require(product_id)
        updated = replace(current, active=active)
        self._products[product_id] = updated
        return updated

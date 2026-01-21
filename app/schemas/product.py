from __future__ import annotations
from pydantic import BaseModel, Field, field_validator

from app.domain.product import ProductID, ProductsCategory, LIMIT_PRICE


class ProductCreator(BaseModel):
    id: ProductID = Field(gt=1)
    name: str = Field(min_length=1)
    description: str | None = None
    price: float = Field(ge=0.0)
    category: ProductsCategory = ProductsCategory.UNCATEGORIZED
    stock: int = Field(ge=0)
    active: bool = True

    @field_validator("name", mode="before")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        value = value.strip().title()
        if not value:
            raise ValueError("Nome não pode ser vazio")
        return value

    @field_validator("description", mode="before")
    @classmethod
    def normalize_description(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip().capitalize()
        return value

    @field_validator("price", mode="before")
    @classmethod
    def validate_price(cls, value: float) -> float:
        if value > LIMIT_PRICE:
            raise ValueError(f"Preço não pode ser maior que {LIMIT_PRICE}")
        return value

    @field_validator("stock")
    @classmethod
    def service_has_no_stock(cls, value: int, info):
        if info.data.get("category") == ProductsCategory.SERVICO and value > 0:
            raise ValueError("Serviços não devem ter estoque")
        return value

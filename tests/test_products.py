from app.domain.product import Product, ProductId, ProductsCategory


def test_product_entity_creation():
    product = Product(
        id=ProductId(1),
        name="Test Product",
        description="This is a test product.",
        price=9999.99,
        category=ProductsCategory.ELETRONICO,
        stock=100,
        active=True,
    )

    assert product.id == ProductId(1)
    assert product.name == "Test Product"
    assert product.description == "This is a test product."
    assert product.price == 9999.99
    assert product.category == ProductsCategory.ELETRONICO
    assert product.stock == 100
    assert product.active is True


def test_product_entity_immutability():
    product = Product(
        id=ProductId(2),
        name="Immutable Product",
        description="This product should be immutable.",
        price=1999.99,
        category=ProductsCategory.LIVROS,
        stock=50,
        active=False,
    )

    try:
        product.name = "New Name"
        assert False, (
            "Expected AttributeError when trying to modify an immutable field."
        )
    except AttributeError:
        pass  # Expected behavior

    try:
        product.price = 2999.99
        assert False, (
            "Expected AttributeError when trying to modify an immutable field."
        )
    except AttributeError:
        pass  # Expected behavior

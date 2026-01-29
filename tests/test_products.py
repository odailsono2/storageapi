from app.domain.product import Product, ProductsCategory, ProductRepository
from app.domain.product import ProductId


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


def test_product_repository_add_and_get():
    repo = ProductRepository()

    product = repo.add(
        name="Repository Product",
        price=499.99,
        stock=20,
        category=ProductsCategory.BELEZA,
        description="Product added via repository.",
        active=True,
    )

    assert repo._products  # só para ver se realmente inseriu algo
    assert list(repo._products.keys()) == [product.id]
    assert repo._products.get(product.id) is not None
    assert product.id == ProductId(1)
    assert product.name == "Repository Product"
    assert product.price == 499.99
    assert product.stock == 20
    assert product.category == ProductsCategory.BELEZA
    assert product.description == "Product added via repository."
    assert product.active is True

    # fetched_product = repo._products.get(product.id)
    fetched_product = repo.get_by_id(product.id)
    assert fetched_product is not None

    assert fetched_product == product


def test_product_repository_list():
    repo = ProductRepository()

    repo.add(
        name="Product 1",
        price=100.0,
        stock=10,
        category=ProductsCategory.ELETRONICO,
    )
    repo.add(
        name="Product 2",
        price=200.0,
        stock=0,
        category=ProductsCategory.LIVROS,
        active=False,
    )
    repo.add(
        name="Product 3",
        price=150.0,
        stock=5,
        category=ProductsCategory.ELETRONICO,
    )

    all_products = repo.list()
    assert len(all_products) == 3

    eletronic_products = repo.list(category=ProductsCategory.ELETRONICO)
    assert len(eletronic_products) == 2

    active_products = repo.list(active=True)
    assert len(active_products) == 2

    priced_products = repo.list(min_price=120.0, max_price=180.0)
    assert len(priced_products) == 1
    assert priced_products[0].name == "Product 3"


def test_product_repository_pagination():
    repo = ProductRepository()

    for i in range(30):
        repo.add(
            name=f"Product {i + 1}",
            price=50.0 + i * 10,
            stock=5 + i,
            category=ProductsCategory.UNCATEGORIZED,
        )

    first_page = repo.list(limit=10, offset=0)
    assert len(first_page) == 10
    assert first_page[0].name == "Product 1"
    assert first_page[-1].name == "Product 10"

    second_page = repo.list(limit=10, offset=10)
    assert len(second_page) == 10
    assert second_page[0].name == "Product 11"
    assert second_page[-1].name == "Product 20"

    third_page = repo.list(limit=10, offset=20)
    assert len(third_page) == 10
    assert third_page[0].name == "Product 21"
    assert third_page[-1].name == "Product 30"


def test_product_repository_list_min_stock():
    repo = ProductRepository()

    repo.add(
        name="Product A",
        price=120.0,
        stock=0,
        category=ProductsCategory.BELEZA,
    )
    repo.add(
        name="Product B",
        price=250.0,
        stock=15,
        category=ProductsCategory.BELEZA,
    )
    repo.add(
        name="Product C",
        price=300.0,
        stock=30,
        category=ProductsCategory.BELEZA,
    )

    products_with_min_stock_10 = repo.list(min_stock=10)
    assert len(products_with_min_stock_10) == 2
    assert all(p.stock >= 10 for p in products_with_min_stock_10)


def test_change_active_status():
    repo = ProductRepository()

    product = repo.add(
        name="Active Product",
        price=150.0,
        stock=20,
        category=ProductsCategory.UNCATEGORIZED,
        active=True,
    )

    assert product.active is True

    # Simulate changing the active status
    updated_product = Product(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        category=product.category,
        stock=product.stock,
        active=False,
    )

    repo._products[product.id] = updated_product

    fetched_product = repo.get_by_id(product.id)
    assert fetched_product is not None
    assert fetched_product.active is False

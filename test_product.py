import pytest

from products import LimitedProduct, NonStockedProduct, Product
from store import Store


def test_create_product_with_valid_details():
    product = Product("MacBook Air M2", price=1450, quantity=100)

    assert product.name == "MacBook Air M2"
    assert product.price == 1450
    assert product.quantity == 100
    assert product.is_active()


def test_create_product_with_invalid_details_raises_exception():
    with pytest.raises(ValueError):
        Product("", price=1450, quantity=100)

    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=-10, quantity=100)


def test_product_becomes_inactive_when_quantity_reaches_zero():
    product = Product("MacBook Air M2", price=1450, quantity=1)

    product.buy(1)

    assert product.quantity == 0
    assert not product.is_active()


def test_buy_product_updates_quantity_and_returns_success_message():
    product = Product("MacBook Air M2", price=1450, quantity=5)

    result = product.buy(2)

    assert product.quantity == 3
    assert result == "Successfully bought 2 MacBook Air M2(s)."


def test_buying_more_than_available_quantity_raises_exception():
    product = Product("MacBook Air M2", price=1450, quantity=2)

    with pytest.raises(ValueError):
        product.buy(3)

    assert product.quantity == 2


def test_non_stocked_product_initializes_and_shows_its_characteristic(capsys):
    product = NonStockedProduct("Windows License", price=125)

    assert isinstance(product, Product)
    assert product.quantity == 0

    product.show()

    assert "This product is non-stocked." in capsys.readouterr().out


def test_limited_product_initializes_and_shows_its_maximum(capsys):
    product = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)

    assert isinstance(product, Product)
    assert product.quantity == 250
    assert product.maximum == 1

    product.show()

    assert "Limited to 1 per order." in capsys.readouterr().out


def test_store_accepts_the_new_product_types():
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
        NonStockedProduct("Windows License", price=125),
        LimitedProduct("Shipping", price=10, quantity=250, maximum=1),
    ]

    best_buy = Store(product_list)

    assert best_buy.products == product_list
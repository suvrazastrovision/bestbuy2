import pytest

from products import LimitedProduct, NonStockedProduct, Product
from promotions import PercentDiscount, Promotion, SecondHalfPrice, ThirdOneFree
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
    assert product.last_purchase_price == 2900
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


def test_promotion_is_abstract():
    with pytest.raises(TypeError):
        Promotion("Generic promotion")


@pytest.mark.parametrize(
    ("promotion", "quantity", "expected_price"),
    [
        (PercentDiscount("30% off!", percent=30), 2, 2030.0),
        (SecondHalfPrice("Second Half price!"), 3, 3625.0),
        (ThirdOneFree("Third One Free!"), 3, 2900.0),
    ],
)
def test_promotions_calculate_discounted_total(promotion, quantity, expected_price):
    product = Product("MacBook Air M2", price=1450, quantity=10)

    assert promotion.apply_promotion(product, quantity) == pytest.approx(expected_price)


def test_product_can_add_remove_and_show_promotion(capsys):
    product = Product("MacBook Air M2", price=1450, quantity=10)
    promotion = PercentDiscount("30% off!", percent=30)

    product.set_promotion(promotion)
    assert product.get_promotion() is promotion

    product.show()
    assert "Promotion: 30% off!" in capsys.readouterr().out

    product.set_promotion(None)
    assert product.get_promotion() is None


def test_store_order_uses_product_promotion():
    product = Product("MacBook Air M2", price=1450, quantity=10)
    product.set_promotion(SecondHalfPrice("Second Half price!"))
    best_buy = Store([product])

    assert best_buy.order([(product, 3)]) == 3625.0
    assert product.quantity == 7


def test_buy_records_discounted_price_for_current_promotion():
    product = Product("MacBook Air M2", price=1450, quantity=10)
    product.set_promotion(ThirdOneFree("Third One Free!"))

    product.buy(3)

    assert product.last_purchase_price == 2900


@pytest.mark.parametrize(
    "percent", [-1, 101, float("nan"), float("inf"), "30", 10**1000]
)
def test_percent_discount_rejects_invalid_percentage(percent):
    with pytest.raises(ValueError):
        PercentDiscount("Invalid discount", percent=percent)


@pytest.mark.parametrize(
    ("promotion", "quantity", "expected_price"),
    [
        (PercentDiscount("30% off", 30), 2, 2030.0),
        (SecondHalfPrice("Second item half price"), 3, 3625.0),
        (ThirdOneFree("Buy two, get one free"), 3, 2900.0),
    ],
)
def test_store_order_uses_each_promotion(promotion, quantity, expected_price):
    product = Product("MacBook Air M2", price=1450, quantity=10)
    product.set_promotion(promotion)

    assert Store([product]).order([(product, quantity)]) == pytest.approx(expected_price)
    assert product.quantity == 10 - quantity
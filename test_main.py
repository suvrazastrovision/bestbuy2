import main
from products import Product
from promotions import PercentDiscount, SecondHalfPrice
from store import Store


def test_initial_products_have_promotions():
    assert all(
        product.get_promotion() is not None for product in main.best_buy.products
    )


def test_manage_promotions_assigns_selected_promotion(monkeypatch, capsys):
    product = Product("MacBook Air M2", price=1450, quantity=10)
    store = Store([product])
    answers = iter(["1", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    main.manage_promotions(store)

    assert isinstance(product.get_promotion(), SecondHalfPrice)
    assert "Second item half price promotion applied" in capsys.readouterr().out


def test_manage_promotions_displays_assigned_offer(monkeypatch, capsys):
    product = Product("MacBook Air M2", price=1450, quantity=10)
    product.set_promotion(PercentDiscount("30% off", 30))
    monkeypatch.setattr("builtins.input", lambda _: "1")

    main.list_products(Store([product]))

    assert "Promotion: 30% off" in capsys.readouterr().out


def test_manage_promotions_rejects_product_number_zero(monkeypatch, capsys):
    product = Product("MacBook Air M2", price=1450, quantity=10)
    monkeypatch.setattr("builtins.input", lambda _: "0")

    main.manage_promotions(Store([product]))

    assert product.get_promotion() is None
    assert "Invalid product number." in capsys.readouterr().out


def test_start_applies_promotion_to_order(monkeypatch, capsys):
    product = Product("MacBook Air M2", price=1450, quantity=10)
    store = Store([product])
    answers = iter(["4", "1", "1", "30", "3", "1", "2", "", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    main.start(store)

    assert product.quantity == 8
    assert "Order cost: 2030.00 dollars." in capsys.readouterr().out

# Best Buy Store

A small Python store inventory app with product types and purchase promotions.

## OOP and logic

- **Encapsulation:** products manage their stock and optional promotion.
- **Inheritance:** non-stocked and limited products extend `Product`.
- **Polymorphism:** product types customize `show`; promotion types calculate discounts differently.
- **Abstraction:** `Promotion` defines the common promotion interface.
- **Store logic:** inventory tracks available products, validates orders, updates stock, and calculates totals with percentage-off, second-item-half-price, or buy-two-get-one-free promotions.

Run the app with `python main.py`. Run tests with `python -m pytest test_product.py`.

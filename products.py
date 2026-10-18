from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from promotions import Promotion


class Product:
    """A product with stock, pricing, and an optional promotion."""

    def __init__(self, name, price, quantity):
        """Create a product with its name, unit price, and stock quantity."""
        if not name:
            raise ValueError("Product name cannot be empty.")
        if price < 0:
            raise ValueError("Product price cannot be negative.")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.promotion: Promotion | None = None
        self.last_purchase_price = 0.0

    def display_info(self):
        """Return a one-line description of the product."""
        return (
            f"Product Name: {self.name}, Price: EUR{self.price:.2f}, "
            f"Quantity: {self.quantity}"
        )

    def buy(self, amount):
        """Buy the requested amount, recording its price and reducing stock."""
        if amount > self.quantity:
            raise ValueError("Insufficient quantity.")

        if 0 < amount <= self.quantity:
            if self.promotion is None:
                self.last_purchase_price = self.price * amount
            else:
                self.last_purchase_price = self.promotion.apply_promotion(
                    self, amount
                )
            self.quantity -= amount
            return f"Successfully bought {amount} {self.name}(s)."
        else:
            return "Invalid purchase amount or insufficient quantity."

    def is_active(self):
        """Return whether the product has stock available."""
        return self.quantity > 0

    def show(self):
        """Print product details and its promotion, if present."""
        print(self.display_info())
        if self.promotion is not None:
            print(f"Promotion: {self.promotion.name}")

    def get_promotion(self) -> Promotion | None:
        """Return the product's current promotion, if any."""
        return self.promotion

    def set_promotion(self, promotion: Promotion | None) -> None:
        """Set or remove the product's promotion."""
        self.promotion = promotion

    def set_quantity(self, new_quantity):
        """Update stock when the new quantity is non-negative."""
        if new_quantity >= 0:
            self.quantity = new_quantity
        else:
            print("Invalid quantity. Please enter a non-negative value.")


class NonStockedProduct(Product):
    """A product that is not represented by physical store stock."""

    def __init__(self, name, price):
        """Create a non-stocked product."""
        super().__init__(name, price, quantity=0)

    def show(self):
        """Print product details and identify it as non-stocked."""
        super().show()
        print("This product is non-stocked.")


class LimitedProduct(Product):
    """A stocked product with a per-order purchase limit."""

    def __init__(self, name, price, quantity, maximum):
        """Create a limited product with its maximum order quantity."""
        super().__init__(name, price, quantity)
        self.maximum = maximum

    def show(self):
        """Print product details and its per-order limit."""
        super().show()
        print(f"Limited to {self.maximum} per order.")

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from promotions import Promotion


class Product:
    def __init__(self, name, price, quantity):
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
        return f"Product Name: {self.name}, Price: EUR{self.price:.2f}, Quantity: {self.quantity}"

    def buy(self, amount):
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
        return self.quantity > 0

    def show(self):
        print(self.display_info())
        if self.promotion is not None:
            print(f"Promotion: {self.promotion.name}")

    def get_promotion(self) -> Promotion | None:
        return self.promotion

    def set_promotion(self, promotion: Promotion | None) -> None:
        self.promotion = promotion

    def set_quantity(self, new_quantity):
        if new_quantity >= 0:
            self.quantity = new_quantity
        else:
            print("Invalid quantity. Please enter a non-negative value.")


class NonStockedProduct(Product):
    def __init__(self, name, price):
        super().__init__(name, price, quantity=0)

    def show(self):
        super().show()
        print("This product is non-stocked.")


class LimitedProduct(Product):
    def __init__(self, name, price, quantity, maximum):
        super().__init__(name, price, quantity)
        self.maximum = maximum

    def show(self):
        super().show()
        print(f"Limited to {self.maximum} per order.")

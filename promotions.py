from abc import ABC, abstractmethod


class Promotion(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity) -> float:
        """Return the total price after applying this promotion."""


class PercentDiscount(Promotion):
    def __init__(self, name, percent):
        if not 0 <= percent <= 100:
            raise ValueError("Discount percentage must be between 0 and 100.")
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product, quantity) -> float:
        return product.price * quantity * (100 - self.percent) / 100


class SecondHalfPrice(Promotion):
    def apply_promotion(self, product, quantity) -> float:
        full_price_items = quantity // 2 + quantity % 2
        half_price_items = quantity // 2
        return product.price * (full_price_items + half_price_items * 0.5)


class ThirdOneFree(Promotion):
    def apply_promotion(self, product, quantity) -> float:
        return product.price * (quantity - quantity // 3)

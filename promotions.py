from abc import ABC, abstractmethod
import math


class Promotion(ABC):
    """Base interface for product purchase promotions."""

    def __init__(self, name):
        """Create a promotion with a display name."""
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity) -> float:
        """Return the total price for a quantity after applying the offer."""


class PercentDiscount(Promotion):
    """Reduce a purchase total by a fixed percentage."""

    def __init__(self, name, percent):
        """Create a percentage discount between zero and one hundred."""
        try:
            valid_percent = math.isfinite(percent) and 0 <= percent <= 100
        except (TypeError, OverflowError):
            valid_percent = False
        if not valid_percent:
            raise ValueError("Discount percentage must be between 0 and 100.")
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product, quantity) -> float:
        """Calculate the discounted total for the requested quantity."""
        return product.price * quantity * (100 - self.percent) / 100


class SecondHalfPrice(Promotion):
    """Charge half price for every second item purchased."""

    def apply_promotion(self, product, quantity) -> float:
        """Calculate the total with every second item half price."""
        full_price_items = quantity // 2 + quantity % 2
        half_price_items = quantity // 2
        return product.price * (full_price_items + half_price_items * 0.5)


class ThirdOneFree(Promotion):
    """Give one item free for every group of three purchased."""

    def apply_promotion(self, product, quantity) -> float:
        """Calculate the total after removing every third item's cost."""
        return product.price * (quantity - quantity // 3)

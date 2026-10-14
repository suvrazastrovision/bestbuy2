class Store:
    """Manage the products available in a store."""

    def __init__(self, products):
        self.products = list(products)

    def add_product(self, product):
        """Add a product to the store."""
        self.products.append(product)

    def remove_product(self, product):
        """Remove a product from the store."""
        self.products.remove(product)

    def get_total_quantity(self) -> int:
        """Return the total number of items currently in stock."""
        return sum(product.quantity for product in self.products)

    def get_all_products(self):
        """Return all products that currently have stock."""
        return [product for product in self.products if product.is_active()]

    def order(self, shopping_list) -> float:
        """Buy the requested products and return the order's total price."""
        total_price = 0.0

        for product, quantity in shopping_list:
            if product not in self.products:
                raise ValueError(f"{product.name} is not available in this store.")
            if quantity <= 0 or quantity > product.quantity:
                raise ValueError(f"Invalid quantity for {product.name}.")

            product.buy(quantity)
            total_price += product.price * quantity

        return total_price

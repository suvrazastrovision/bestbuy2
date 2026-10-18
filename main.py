import products
import promotions
import store


def list_products(store_obj):
    """Display active products and return them in display order."""
    available_products = store_obj.get_all_products()
    if not available_products:
        print("No active products in store.")
        return available_products

    for number, product in enumerate(available_products, start=1):
        product_info = product.display_info()
        if product.get_promotion() is not None:
            product_info += f", Promotion: {product.get_promotion().name}"
        print(f"{number}. {product_info}")
    return available_products


def manage_promotions(store_obj):
    """Assign or remove a promotion for an active product."""
    available_products = list_products(store_obj)
    if not available_products:
        return

    product_number = input("Choose a product number: ").strip()
    try:
        product_index = int(product_number) - 1
    except ValueError:
        print("Invalid product number.")
        return

    if not 0 <= product_index < len(available_products):
        print("Invalid product number.")
        return
    product = available_products[product_index]

    print("1. Percentage discount")
    print("2. Second item half price")
    print("3. Buy two, get one free")
    print("4. Remove promotion")
    promotion_choice = input("Choose a promotion: ").strip()

    if promotion_choice == "1":
        try:
            percent = float(input("Enter discount percentage (0-100): "))
            promotion = promotions.PercentDiscount(f"{percent:g}% off", percent)
        except ValueError as error:
            print(f"Invalid discount percentage: {error}")
            return
    elif promotion_choice == "2":
        promotion = promotions.SecondHalfPrice("Second item half price")
    elif promotion_choice == "3":
        promotion = promotions.ThirdOneFree("Buy two, get one free")
    elif promotion_choice == "4":
        product.set_promotion(None)
        print(f"Promotion removed from {product.name}.")
        return
    else:
        print("Invalid promotion choice.")
        return

    product.set_promotion(promotion)
    print(f"{promotion.name} promotion applied to {product.name}.")


def make_order(store_obj):
    """Ask the user for products and quantities, then place the order."""
    available_products = list_products(store_obj)
    if not available_products:
        return

    shopping_list = []
    print("Press Enter without a product number to finish the order.")

    while True:
        product_number = input("Which product number do you want? ").strip()
        if not product_number:
            break

        try:
            index = int(product_number) - 1
            if index < 0:
                raise ValueError
            product = available_products[index]
            quantity = int(input("What amount do you want? "))
            if quantity <= 0:
                raise ValueError
            shopping_list.append((product, quantity))
            print("Product added to the order!")
        except (ValueError, IndexError):
            print("Invalid product number or amount. Please try again.")

    if not shopping_list:
        print("No products were ordered.")
        return

    try:
        total_price = store_obj.order(shopping_list)
        print(f"Order cost: {total_price:.2f} dollars.")
    except ValueError as error:
        print(error)


def start(store_obj):
    """Display the menu and handle user choices until Quit is selected."""
    while True:
        print("\nStore Menu")
        print("1. List all products in store")
        print("2. Show total amount in store")
        print("3. Make an order")
        print("4. Manage promotions")
        print("5. Quit")

        choice = input("Please choose an option: ").strip()

        if choice == "1":
            list_products(store_obj)
        elif choice == "2":
            print(f"Total amount in store: {store_obj.get_total_quantity()}")
        elif choice == "3":
            make_order(store_obj)
        elif choice == "4":
            manage_promotions(store_obj)
        elif choice == "5":
            print("Thank you for visiting Best Buy!")
            break
        else:
            print("Invalid option. Please choose a number from 1 to 5.")


# setup initial stock of inventory
product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                products.Product("Google Pixel 7", price=500, quantity=250)]
best_buy = store.Store(product_list)


if __name__ == "__main__":
    start(best_buy)

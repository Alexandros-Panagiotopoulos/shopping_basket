class Item():
    """A class to store all the store's items with their prices (available and unavailable)"""

# we can use an id
# the class should validate that the object can be instantiated (by raising exceptions if the constraints are not met, e.g. price > 0)
# we can also use type hints
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.available = True

    def change_price(self, new_price):
        self.price = new_price

    def set_out_of_stock(self):
        self.available = False

    def set_in_stock(self):
        self.available = True


class Basket():
    """A class with the items in the basket"""

    def __init__(self):
        self.items = {}

    def add_items(self, item, quantity):
        if item.available == True:
            if item in self.items.keys():
                self.items[item] += quantity
            else:
                self.items[item] = quantity
        else:
            raise ItemOutOfStockException()


class Discount():
    """A class to calculate the discount of some items"""

    def __init__(self, items):
        self.items = items

    def calculate_many_of_a_type_discount(self, products):
        discount = 0
        for item in self.items:
            if item.name in products.keys():
                discount += int(self.items[item]/products[item.name]) * item.price
        return discount

    def calculate_percentage_discount(self, products):
        discount = 0
        for item in self.items:
            if item.name in products.keys():
                discount += self.items[item] * item.price * products[item.name]
        return discount

    # def shampoo_discount(self, shampoo_large, shampoo_medium, shampoo_small): #it is considered the smaller the shampoo the lower the price
    #     discount = 0
    #     shampoo_list = []
    #     if shampoo_large in self.basket.keys():
    #         shampoo_list.extend(self.basket[shampoo_large] * [shampoo_large])
    #     if shampoo_medium in self.basket.keys():
    #         shampoo_list.extend(self.basket[shampoo_medium] * [shampoo_medium])
    #     if shampoo_small in self.basket.keys():
    #         shampoo_list.extend(self.basket[shampoo_small] * [shampoo_small])
    #     for i in range(2, len(shampoo_list), 3):
    #         discount += shampoo_list[i].price
    #     return discount


class BasketCostCalculator():
    """A class to calculate the subtotal, discount and total cost"""

    def __init__(self, basket):
        self.basket = basket

    def calculate_subtotal(self):
        subtotal = 0
        for item in self.basket.items:
            subtotal += (item.price * self.basket.items[item])
        return subtotal

    def calculate_total_discount(self, discount, many_of_type_disc, percentage_disc):
        return (discount.calculate_many_of_a_type_discount(many_of_type_disc) + discount.calculate_percentage_discount(percentage_disc))

    def calculate_total(self, discount, many_of_type_disc, percentage_disc):
        return self.calculate_subtotal() - self.calculate_total_discount(discount, many_of_type_disc, percentage_disc)

# define Python user-defined exceptions
class Error(Exception):
   """Base class for other exceptions"""
   pass

class ItemOutOfStockException(Error):
   """Raised when the item is out of stock"""
   pass
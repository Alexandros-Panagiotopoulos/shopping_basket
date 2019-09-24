class Item():
    """A class to store all the store's items with their prices (available and unavailable)"""

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
        self.basket = {}

    def add_items(self, item, quantity):
        if item.available == True:
            if item in self.basket.keys():
                self.basket[item] += quantity
            else:
                self.basket[item] = quantity
        else:
            raise ItemOutOfStockException()


class Discount():
    """A class to calculate the discount of items for the current basket"""

    def __init__(self, basket):
        self.basket = basket

    def many_of_a_type_discount(self, products):
        discount = 0
        for item in self.basket:
            if item.name in products.keys():
                discount += int(self.basket[item]/products[item.name]) * item.price
        return discount

    def percentage_discount(self, products):
        discount = 0
        for item in self.basket:
            if item.name in products.keys():
                discount += self.basket[item] * item.price * products[item.name]
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


class CostCalculation():
    """A class to calculate the subtotal, discount and total cost"""

    def __init__(self, basket):
        self.basket = basket

    def calculate_subtotal(self):
        subtotal = 0
        for item in self.basket:
            subtotal += (item.price * self.basket[item])
        return subtotal

    def calculate_total_discount(self, users_discount, many_of_type_disc, percentage_disc):
        discount = users_discount.many_of_a_type_discount(many_of_type_disc) + users_discount.percentage_discount(percentage_disc)
        return discount

    def calculate_total(self, users_discount, many_of_type_disc, percentage_disc):
        total = self.calculate_subtotal() - self.calculate_total_discount(users_discount, many_of_type_disc, percentage_disc)
        return total

# define Python user-defined exceptions
class Error(Exception):
   """Base class for other exceptions"""
   pass

class ItemOutOfStockException(Error):
   """Raised when the item is out of stock"""
   pass
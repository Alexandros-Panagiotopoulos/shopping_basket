class Item():
    """A class to store all the store's items with their prices (available and unavailable)"""

    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.available = True

    def change_price(self, new_price):
        self.price = new_price

    def out_of_stock(self):
        self.available = False

    def in_stock(self):
        self.available = True


class UsersBasket():
    """A class with the items in the users basket and their subtotal cost"""

    def __init__(self, name):
        self.name = name
        self.basket = {}

    def add_items(self, item, amount):
        if item in self.basket.keys():
            self.basket[item] += amount
        else:
            self.basket[item] = amount

    def remove_single_item(self, item):
        if item in self.basket.keys():
            self.basket[item] -= 1
            if self.basket[item] == 0:
                self.basket.pop(item)

    def remove_type_of_items(self, item):
        if item in self.basket.keys():
            self.basket.pop(item)

    def calculate_subtotal(self):
        subtotal = 0
        for item in self.basket:
            subtotal += (item.price * self.basket[item])
        return subtotal


class UsersDiscount():
    """A class to calculate the discount of the current basket and the total cost"""

    def __init__(self, basket):
        self.discount = 0
        self.basket = basket

    def calculate_total(self, users_basket, baked_beans, sardines, shampoo_large, shampoo_medium, shampoo_small):
        total = users_basket.calculate_subtotal() - self.calculate_total_discount (baked_beans, sardines, shampoo_large, shampoo_medium, shampoo_small)
        return total

    def calculate_total_discount(self, baked_beans, sardines, shampoo_large, shampoo_medium, shampoo_small):
        baked_beans_discount = self.baked_beans_discount(baked_beans)
        sardines_discount = self.sardines_discount(sardines)
        shampoo_discount = self.shampoo_discount(shampoo_large, shampoo_medium, shampoo_small)
        discount = baked_beans_discount + sardines_discount + shampoo_discount
        return discount

    def baked_beans_discount(self, baked_beans):
        discount = 0
        if baked_beans in self.basket.keys():
            discount = int(self.basket[baked_beans]/3) * baked_beans.price
        return discount

    def sardines_discount(self, sardines):
        discount = 0
        if sardines in self.basket.keys():
            discount = self.basket[sardines] * sardines.price / 4
        return discount

    def shampoo_discount(self, shampoo_large, shampoo_medium, shampoo_small): #it is considered the smaller the shampoo the lower the price
        discount = 0
        shampoo_list = []
        if shampoo_large in self.basket.keys():
            shampoo_list.extend(self.basket[shampoo_large] * [shampoo_large])
        if shampoo_medium in self.basket.keys():
            shampoo_list.extend(self.basket[shampoo_medium] * [shampoo_medium])
        if shampoo_small in self.basket.keys():
            shampoo_list.extend(self.basket[shampoo_small] * [shampoo_small])
        for i in range(2, len(shampoo_list), 3):
            discount += shampoo_list[i].price
        return discount






    





        
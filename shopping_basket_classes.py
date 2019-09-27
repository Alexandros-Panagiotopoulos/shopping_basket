class Item():
    """A class to store all the store's items with their prices (available and unavailable)"""

# we can use an id
# the class should validate that the object can be instantiated (by raising exceptions if the constraints are not met, e.g. name must be a string)
# we can also use type hints
    def __init__(self, name, price):
        self.name = name
        self.price = price
        if not price > 0:
            raise NegativePriceDetectedException('the price of the item should be a positive number')
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


class Offer():
    """A class to calculate the offers of some items"""

    def __init__(self, items):
        self.items = items

    def calculate_many_of_a_type_offer(self, products):
        offer = 0
        for item in self.items:
            if item.name in products.keys():
                offer += int(self.items[item]/products[item.name]) * item.price
        return offer

    def calculate_percentage_offer(self, products):
        offer = 0
        for item in self.items:
            if item.name in products.keys():
                offer += self.items[item] * item.price * products[item.name]
        return offer

    def calculate_cheapest_item_offer(self, grouped_products):
        """Offer in which for specific grouped products the cheapest out of three is free"""
        grouped_items = self.manipulate_grouped_products(grouped_products)
        offer = 0
        item_list = []
        for item_group in grouped_items:
            for item in item_group:
                item_list.extend(self.items[item] * [item])
            for i in range(2, len(item_list), 3):
                offer += item_list[i].price
            item_list = []
        return offer

    def manipulate_grouped_products(self, grouped_products):
        """receives a list of lists with product names and returns a list of lists with item type objects 
        that are included in the basket shorted by price to feed the calculate_cheapest_item_offer method"""
        grouped_items = []
        for product_group in grouped_products:
            item_group = []
            for product in product_group:
                for item in self.items.keys():
                    if item.name == product:
                        item_group.append(item)
                        break
            if item_group:
                item_group = sorted(item_group, key=lambda x: x.price, reverse=True)
                grouped_items.append(item_group)      
        return grouped_items


class BasketCostCalculator():
    """A class to calculate the subtotal, discount and total cost"""

    def __init__(self, basket):
        self.basket = basket

    def calculate_subtotal(self):
        subtotal = 0
        for item in self.basket.items:
            subtotal += (item.price * self.basket.items[item])
        subtotal = round(subtotal,3)
        return subtotal

    def calculate_total_discount(self, offer, many_of_type_offer, percentage_offer, grouped_products):
        discount = (offer.calculate_many_of_a_type_offer(many_of_type_offer) + 
                    offer.calculate_percentage_offer(percentage_offer)+
                    offer.calculate_cheapest_item_offer(grouped_products))
        return round(discount,3)

    def calculate_total(self, offer, many_of_type_offer, percentage_offer, grouped_products):
        total = self.calculate_subtotal() - self.calculate_total_discount(offer, many_of_type_offer, percentage_offer, grouped_products)
        return round(total,2)

# define Python user-defined exceptions
class Error(Exception):
   """Base class for other exceptions"""
   pass

class ItemOutOfStockException(Error):
   """Raised when the item is out of stock"""
   pass

class NegativePriceDetectedException(Error):
   """Raised when the price of an item is not positive"""
   pass
import mysql.connector

class Item():
    """A class to store all the store's items with their prices (available and unavailable)"""

# we can use an id
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
        for item_group in grouped_items:
            item_list = []
            for item in item_group:
                item_list.extend(self.items[item] * [item])
            for i in range(2, len(item_list), 3):
                offer += item_list[i].price
        return offer

    def manipulate_grouped_products(self, grouped_products):
        """receives a list of lists with product names and returns a list of lists with item type objects 
        that are included in the basket sorted by price to feed the calculate_cheapest_item_offer method"""
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


class CatalogueRepository():
    """A class responsible for fetching catalogue data.
       If the data belongs to our team then the data can be retrieved by accessing the Database.
       If the data is managed by another team then we can fetch them from a (hopefully) RESTful API that they'll expose.
    """

    def __init__(self):
        with open ('database_access.txt') as file_object:
            lines = file_object.read().splitlines()

        host = lines[0]
        user = lines[1]
        passwd = lines[2]
        database = lines[3]

        self.db = mysql.connector.connect(
        host = host,
        user = user,
        passwd = passwd,
        database = database
        )

        self.cursor = self.db.cursor()

    def get_items(self):
        self.cursor.execute("SELECT name, price FROM products")
        products = self.cursor.fetchall()
        items_by_name = {}
        for product in products:
            items_by_name[product[0]] = Item(product[0], float(product[1]))
        self.items_by_name = items_by_name

    def get_many_of_type_offer_products(self):
        self.cursor.execute("SELECT p.name, m.offer_size\
             FROM products AS p INNER JOIN many_of_type_offer AS m ON p.id = m.item_id")
        products = self.cursor.fetchall()
        many_of_type_offer = {}
        for product in products:
            many_of_type_offer[product[0]] = float(product[1])
        return many_of_type_offer

    def get_percentage_offer_products(self):
        self.cursor.execute("SELECT p.name, o.offer_size\
             FROM products AS p INNER JOIN percentage_offer AS o ON p.id = o.item_id")
        products = self.cursor.fetchall()
        percentage_offer = {}
        for product in products:
            percentage_offer[product[0]] = float(product[1])
        return percentage_offer

    def get_cheapest_product_offer_products(self):
        self.cursor.execute("SELECT p.name, c.grouped_products_id \
            FROM products AS p INNER JOIN cheapest_item_offer AS c ON p.id = c.item_id\
                ORDER BY c.grouped_products_id")

        products = self.cursor.fetchall()

        cheapest_item_offer = []
        grouped_id = products[0][1]
        grouped_products = []
        for product in products:
            new_grouped_id = product[1]
            if new_grouped_id != grouped_id:
               grouped_id = new_grouped_id
               cheapest_item_offer.append(grouped_products)
               grouped_products = []
            grouped_products.append(product[0])
        cheapest_item_offer.append(grouped_products)
        return cheapest_item_offer

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
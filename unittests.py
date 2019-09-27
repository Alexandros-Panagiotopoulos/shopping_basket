import unittest
from shopping_basket_classes import Item, Basket, Offer, BasketCostCalculator, NegativePriceDetectedException,ItemOutOfStockException

class TestItem(unittest.TestCase):
    """Test for the class Item"""

    def test_can_create_item_with_positive_price(self):
        price = 0.01
        baked_beans = Item("Baked Beans", price)

        self.assertIsInstance(baked_beans, Item)

    def test_cannot_create_item_with_negative_price(self):
        price = -0.01

        with self.assertRaises(NegativePriceDetectedException) as error:
            Item("Baked Beans", price)
        self.assertEqual('the price of the item should be a positive number', str(error.exception))

    def test_cannot_create_item_with_zero_price(self):
        price = 0

        with self.assertRaises(NegativePriceDetectedException) as error:
            Item("Baked Beans", price)
        self.assertEqual('the price of the item should be a positive number', str(error.exception))

class TestBasket(unittest.TestCase):
    """Test for the class Basket"""

    def test_can_insert_items_into_empty_basket(self):
        baked_beans = Item("Baked Beans", 0.99)
        basket = Basket()
        basket.add_items(baked_beans, 4)

        self.assertEqual(basket.items,{baked_beans: 4})

    def test_can_add_items_of_the_same_type_into_basket(self):
        baked_beans = Item("Baked Beans", 0.99)
        basket = Basket()
        basket.add_items(baked_beans, 4)
        basket.add_items(baked_beans, 1)

        self.assertEqual(basket.items,{baked_beans: 5})

    def test_cannot_add_unavailable_items_into_basket(self):
        baked_beans = Item("Baked Beans", 0.99)
        baked_beans.set_out_of_stock()
        basket = Basket()

        self.assertRaises(ItemOutOfStockException, basket.add_items, baked_beans, 1)


class TestOffer(unittest.TestCase):
    """Test for the class Offer"""

    def setUp(self):
        """Define the catalogue of items and basket"""

        self.baked_beans = Item("Baked Beans", 0.99)
        self.biscuits  = Item("Biscuits", 1.20)
        self.sardines  = Item("Sardines", 1.89)
        self.shampoo_small  = Item("Shampoo (Small)", 2.00)
        self.shampoo_medium = Item("Shampoo (Medium)", 2.50)
        self.shampoo_large = Item("Shampoo (Large)", 3.50)
        self.basket = Basket()

    def test_calculate_three_baked_beans_offer(self):
        self.basket.add_items(self.baked_beans, 4)
        many_of_type_offer = {"Baked Beans" : 3, "Biscuits": 5} #Offer a baked bean for every 3 and a biscuit for every 5
        users_offer = Offer(self.basket.items)
        discount_amount = users_offer.calculate_many_of_a_type_offer(many_of_type_offer)

        self.assertEqual(discount_amount, 0.99)

    def test_calculate_baked_beans_and_biscuit_offer(self):
        self.basket.add_items(self.baked_beans, 4)
        self.basket.add_items(self.biscuits, 22)
        many_of_type_offer = {"Baked Beans" : 3, "Biscuits": 5}
        users_offer = Offer(self.basket.items)
        discount_amount = users_offer.calculate_many_of_a_type_offer(many_of_type_offer)

        self.assertEqual(discount_amount, 5.79) #(Biscuit: 22%5 = 4, 4*1.20 = 4.80) (4%3 = 1, 1*0.99 = 0.99)

    def test_calculate_sardines_percentage_offer(self):
        self.basket.add_items(self.sardines, 4)
        percentage_offer = {"Sardines" : 0.25}
        users_offer = Offer(self.basket.items)
        discount_amount = users_offer.calculate_percentage_offer(percentage_offer)

        self.assertEqual(discount_amount, 1.89) #(0.25*1.89)*4

    def test_calculate_cheapest_item_offer(self):
        self.basket.add_items(self.shampoo_large, 3)
        self.basket.add_items(self.shampoo_medium, 1)
        self.basket.add_items(self.shampoo_small, 2)
        cheapest_item_offer = [["Shampoo (Small)", "Shampoo (Medium)", "Shampoo (Large)"], ["Sardines", "Biscuits"]]
        users_offer = Offer(self.basket.items)
        discount_amount = users_offer.calculate_cheapest_item_offer(cheapest_item_offer)

        self.assertEqual(discount_amount, 5.5)

    def test_calculate_cheapest_item_offer_for_two_groups(self):
        self.basket.add_items(self.shampoo_large, 3)
        self.basket.add_items(self.shampoo_medium, 1)
        self.basket.add_items(self.shampoo_small, 2)
        self.basket.add_items(self.sardines, 4)
        self.basket.add_items(self.biscuits, 3)
        cheapest_item_offer = [["Shampoo (Small)", "Shampoo (Medium)", "Shampoo (Large)"], ["Sardines", "Biscuits"]]
        users_offer = Offer(self.basket.items)
        discount_amount = users_offer.calculate_cheapest_item_offer(cheapest_item_offer)

        self.assertEqual(discount_amount, 8.59)


class TestBasketCostCalculator(unittest.TestCase):
    """Test for the class BasketCostCalculator"""

    def setUp(self):
        """Define the catalogue of items, basket and current offers"""

        self.baked_beans = Item("Baked Beans", 0.99)
        self.biscuits  = Item("Biscuits", 1.20)
        self.sardines  = Item("Sardines", 1.89)
        self.shampoo_small  = Item("Shampoo (Small)", 2.00)
        self.shampoo_medium = Item("Shampoo (Medium)", 2.50)
        self.shampoo_large = Item("Shampoo (Large)", 3.50)
        self.basket = Basket()
        self.many_of_type_offer = {"Baked Beans" : 3}
        self.percentage_offer = {"Sardines" : 0.25}
        self.cheapest_item_offer = [["Shampoo (Small)", "Shampoo (Medium)", "Shampoo (Large)"]]
        self.users_offer = Offer(self.basket.items)
        self.cost = BasketCostCalculator(self.basket)

    def test_costs_baked_beans_sardines(self):
        self.basket.add_items(self.baked_beans, 4)
        self.basket.add_items(self.biscuits, 1)
        subtotal = self.cost.calculate_subtotal()
        discount = self.cost.calculate_total_discount(self.users_offer, self.many_of_type_offer, self.percentage_offer, self.cheapest_item_offer)
        total = self.cost.calculate_total(self.users_offer, self.many_of_type_offer, self.percentage_offer, self.cheapest_item_offer)

        self.assertEqual(subtotal, 5.16)
        self.assertEqual(discount, 0.99)
        self.assertEqual(total, 4.17)

    def test_costs_baked_beans_biscuits_sardines(self):
        self.basket.add_items(self.baked_beans, 2)
        self.basket.add_items(self.biscuits, 1)
        self.basket.add_items(self.sardines, 2)
        subtotal = self.cost.calculate_subtotal()
        discount = self.cost.calculate_total_discount(self.users_offer, self.many_of_type_offer, self.percentage_offer, self.cheapest_item_offer)
        total = self.cost.calculate_total(self.users_offer, self.many_of_type_offer, self.percentage_offer, self.cheapest_item_offer)

        self.assertEqual(subtotal, 6.96)
        self.assertEqual(discount, 0.945)
        self.assertEqual(total, 6.01)

    def test_costs_of_shampoos(self):
        self.basket.add_items(self.shampoo_large, 3)
        self.basket.add_items(self.shampoo_medium, 1)
        self.basket.add_items(self.shampoo_small, 2)
        subtotal = self.cost.calculate_subtotal()
        discount = self.cost.calculate_total_discount(self.users_offer, self.many_of_type_offer, self.percentage_offer, self.cheapest_item_offer)
        total = self.cost.calculate_total(self.users_offer, self.many_of_type_offer, self.percentage_offer, self.cheapest_item_offer)

        self.assertEqual(subtotal, 17.0)
        self.assertEqual(discount, 5.5)
        self.assertEqual(total, 11.5)


unittest.main()
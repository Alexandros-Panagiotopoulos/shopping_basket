from shopping_basket_classes import Item, Basket, Offer, BasketCostCalculator, ItemOutOfStockException, CatalogueRepository

catalogue = CatalogueRepository()
catalogue.get_items()

#Products with discount
many_of_type_offer = catalogue.get_many_of_type_offer_products()
percentage_offer = catalogue.get_percentage_offer_products()
cheapest_item_offer = catalogue.get_cheapest_product_offer_products()

#Basket chosen by client
basket = Basket()
try:
    basket.add_items(catalogue.items_by_name["Baked Beans"], 4)
except ItemOutOfStockException:
    print('Sorry, the item is currently out of stock')

try:
    basket.add_items(catalogue.items_by_name["Biscuits"], 1)
except ItemOutOfStockException:
    print('Sorry, the item is currently out of stock')

users_offer = Offer(basket.items)
cost = BasketCostCalculator(basket)

subtotal = cost.calculate_subtotal()

# in a real project calculate_total_discount() would accept a list of OfferStrategies and iterate through all of them.
discount = cost.calculate_total_discount(users_offer, many_of_type_offer, percentage_offer, cheapest_item_offer)
total = cost.calculate_total(users_offer, many_of_type_offer, percentage_offer, cheapest_item_offer)

print (subtotal, discount, total)
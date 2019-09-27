from shopping_basket_classes import Item, Basket, Offer, BasketCostCalculator, ItemOutOfStockException, CatalogueRepository

#Products with discount
many_of_type_offer = {"Baked Beans" : 3}
percentage_offer = {"Sardines" : 0.25}
cheapest_item_offer = [["Shampoo (Small)", "Shampoo (Medium)", "Shampoo (Large)"]]
catalogue = CatalogueRepository()

#Basket chosen by client
basket = Basket()
try:
    basket.add_items(catalogue.get_item_by_name("baked_beans"), 4)
except ItemOutOfStockException:
    print('Sorry, the item is currently out of stock')

try:
    basket.add_items(catalogue.get_item_by_name("biscuits"), 1)
except ItemOutOfStockException:
    print('Sorry, the item is currently out of stock')

users_offer = Offer(basket.items)
cost = BasketCostCalculator(basket)

subtotal = cost.calculate_subtotal()

# in a real project calculate_total_discount() would accept a list of OfferStrategies and iterate through all of them.
discount = cost.calculate_total_discount(users_offer, many_of_type_offer, percentage_offer, cheapest_item_offer)
total = cost.calculate_total(users_offer, many_of_type_offer, percentage_offer, cheapest_item_offer)

print (subtotal, discount, total)
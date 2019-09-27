from shopping_basket_classes import Item, Basket, Offer, BasketCostCalculator, ItemOutOfStockException

#Store's Ctalogue of items
baked_beans = Item("Baked Beans", 0.99)
biscuits  = Item("Biscuits", 1.20)
sardines  = Item("Sardines", 1.89)
shampoo_small  = Item("Shampoo (Small)", 2.00)
shampoo_medium = Item("Shampoo (Medium)", 2.50)
shampoo_large = Item("Shampoo (Large)", 3.50)

#Products with discount
many_of_type_offer = {"Baked Beans" : 3}
percentage_offer = {"Sardines" : 0.25}
cheapest_item_offer = [["Shampoo (Small)", "Shampoo (Medium)", "Shampoo (Large)"]]

#Basket chosen by client
basket = Basket()
try:
    basket.add_items(baked_beans, 4)
except ItemOutOfStockException:
    print('Sorry, the item is currently out of stock')

try:
    basket.add_items(biscuits, 1)
except ItemOutOfStockException:
    print('Sorry, the item is currently out of stock')

users_offer = Offer(basket.items)
cost = BasketCostCalculator(basket)

subtotal = cost.calculate_subtotal()
discount = cost.calculate_total_discount(users_offer, many_of_type_offer, percentage_offer, cheapest_item_offer)
total = cost.calculate_total(users_offer, many_of_type_offer, percentage_offer, cheapest_item_offer)

print (subtotal, discount, total)
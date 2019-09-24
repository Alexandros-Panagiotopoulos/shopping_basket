from shopping_basket_classes import Item, Basket, Discount, BasketCostCalculator, ItemOutOfStockException

#Store's items
baked_beans = Item("Baked Beans", 0.99)
biscuits  = Item("Biscuits", 1.20)
# biscuits.set_out_of_stock()
sardines  = Item("Sardines", 1.89)
shampoo_small  = Item("Shampoo (Small)", 2.00)
shampoo_medium = Item("Shampoo (Medium)", 2.50)
shampoo_large = Item("Shampoo (Large)", 3.50)

#Products with discount
many_of_type_disc = {"Baked Beans" : 3}
percentage_disc = {"Sardines" : 0.25}

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

# basket = Basket()
# basket.add_items(baked_beans, 2)
# basket.add_items(biscuits, 1)
# basket.add_items(sardines, 2)

# basket = Basket()
# basket.add_items(shampoo_large, 3)
# basket.add_items(shampoo_medium, 1)
# basket.add_items(shampoo_small, 2)

users_discount = Discount(basket.items)
cost = BasketCostCalculator(basket)

subtotal = cost.calculate_subtotal()
discount = cost.calculate_total_discount(users_discount, many_of_type_disc, percentage_disc)
total = cost.calculate_total(users_discount, many_of_type_disc, percentage_disc)

print (subtotal, discount, total)
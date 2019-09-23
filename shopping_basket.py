from shopping_basket_classes import Item, UsersBasket, UsersDiscount

baked_beans = Item("Baked Beans", 0.99)
biscuits  = Item("Biscuits", 1.20)
sardines  = Item("Sardines", 1.89)
shampoo_small  = Item("Shampoo (Small)", 2.00)
shampoo_medium = Item("Shampoo (Medium)", 2.50)
shampoo_large = Item("Shampoo (Large)", 3.50)

# users_basket = UsersBasket("Basket 1")
# users_basket.add_items(baked_beans, 4)
# users_basket.add_items(biscuits, 1)
# subtotal = users_basket.calculate_subtotal()

# users_basket = UsersBasket("Basket 2")
# users_basket.add_items(baked_beans, 2)
# users_basket.add_items(biscuits, 1)
# users_basket.add_items(sardines, 2)
# subtotal = users_basket.calculate_subtotal()

users_basket = UsersBasket("Basket 3")
users_basket.add_items(shampoo_large, 3)
users_basket.add_items(shampoo_medium, 1)
users_basket.add_items(shampoo_small, 2)

subtotal = users_basket.calculate_subtotal()
users_discount = UsersDiscount(users_basket.basket)

discount = users_discount.calculate_total_discount(baked_beans, sardines, shampoo_large, shampoo_medium, shampoo_small)
total = users_discount.calculate_total(users_basket, baked_beans, sardines, shampoo_large, shampoo_medium, shampoo_small)

print (subtotal, discount, total)
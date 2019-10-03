import mysql.connector

with open ('c:/Users/alex/code/python/Shopping_basket/database_access.txt') as file_object:
    lines = file_object.read().splitlines()

host = lines[0]
user = lines[1]
passwd = lines[2]
database = lines[3]

mydb = mysql.connector.connect(
host = host,
user = user,
passwd = passwd,
database = database
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE products (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), price VARCHAR(255))")
mycursor.execute("CREATE TABLE many_of_type_offer\
     (id INT AUTO_INCREMENT PRIMARY KEY, item_id INT NOT NULL, offer_size INT NOT NULL,\
        FOREIGN KEY (item_id) REFERENCES products(id))")
mycursor.execute("CREATE TABLE percentage_offer\
     (id INT AUTO_INCREMENT PRIMARY KEY, item_id INT NOT NULL, offer_size VARCHAR(255),\
        FOREIGN KEY (item_id) REFERENCES products(id))")
mycursor.execute("CREATE TABLE cheapest_item_offer\
     (id INT AUTO_INCREMENT PRIMARY KEY, grouped_products_id INT NOT NULL, item_id INT NOT NULL,\
        FOREIGN KEY (item_id) REFERENCES products(id))")

sql = "INSERT INTO products (name, price) VALUES (%s, %s)"
val = [
("Baked Beans", 0.99),
("Biscuits", 1.20),
("Sardines", 1.89),
("Shampoo (Small)", 2.00),
("Shampoo (Medium)", 2.50),
("Shampoo (Large)", 3.50)
]
mycursor.executemany(sql, val)

mydb.commit()

sql = "INSERT INTO many_of_type_offer (item_id, offer_size) VALUES (%s, %s)"
val = (19, 3)

mycursor.execute(sql, val)

mydb.commit()

sql = "INSERT INTO percentage_offer (item_id, offer_size) VALUES (%s, %s)"
val = (21, 0.25)

mycursor.execute(sql, val)

mydb.commit()

sql = "INSERT INTO cheapest_item_offer (grouped_products_id, item_id) VALUES (%s, %s)"
val = [
(1, 22),
(1, 23),
(1, 24)
]
mycursor.executemany(sql, val)

mydb.commit()
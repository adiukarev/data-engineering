# Самостоятельно выбрать предметную область.
# Подобрать пару наборов данных разных форматов.
# Заполнение данных в mongo осуществляем из файлов.
# Реализовать выполнение по 5 запросов в каждой категорий:
# -	выборка (задание 1),
# -	выбора с агрегацией (задание 2)
# -	обновление/удаление данных (задание 3).

from pymongo import MongoClient
from bson.json_util import dumps

client = MongoClient("mongodb://localhost:27017/")
db = client["restaurant"]
menu_collection = db["menu"]
orders_collection = db["orders"]

query_1_1 = list(menu_collection.find({"category": "Main Course"}))
query_1_2 = list(orders_collection.find({"customer_name": "John Doe"}))
query_1_3 = list(orders_collection.find({"order_date": {"$gt": "2023-01-01"}}))
query_1_4 = list(orders_collection.find({"item_id": 1}))
query_1_5 = list(menu_collection.find({"price": {"$gt": 20}}))

with open("query_1_1.json", "w") as f:
    f.write(dumps(query_1_1, indent=4))
with open("query_1_2.json", "w") as f:
    f.write(dumps(query_1_2, indent=4))
with open("query_1_3.json", "w") as f:
    f.write(dumps(query_1_3, indent=4))
with open("query_1_4.json", "w") as f:
    f.write(dumps(query_1_4, indent=4))
with open("query_1_5.json", "w") as f:
    f.write(dumps(query_1_5, indent=4))

query_2_1 = list(orders_collection.aggregate([
    {"$group": {"_id": "$item_id", "total_revenue": {"$sum": {"$multiply": ["$quantity", {"$toDouble": "$item_id"}]}}}}
]))
query_2_2 = list(orders_collection.aggregate([
    {"$group": {"_id": "$customer_name", "total_orders": {"$sum": 1}}}
]))
query_2_3 = list(menu_collection.aggregate([
    {"$group": {"_id": "$category", "average_price": {"$avg": "$price"}}}
]))
query_2_4 = list(orders_collection.aggregate([
    {"$lookup": {"from": "menu", "localField": "item_id", "foreignField": "item_id", "as": "menu_item"}},
    {"$unwind": "$menu_item"},
    {"$group": {"_id": "$menu_item.category", "total_revenue": {"$sum": {"$multiply": ["$quantity", "$menu_item.price"]}}}}
]))
query_2_5 = list(orders_collection.aggregate([
    {"$group": {"_id": "$item_id", "total_quantity": {"$sum": "$quantity"}}}
]))

with open("query_2_1.json", "w") as f:
    f.write(dumps(query_2_1, indent=4))
with open("query_2_2.json", "w") as f:
    f.write(dumps(query_2_2, indent=4))
with open("query_2_3.json", "w") as f:
    f.write(dumps(query_2_3, indent=4))
with open("query_2_4.json", "w") as f:
    f.write(dumps(query_2_4, indent=4))
with open("query_2_5.json", "w") as f:
    f.write(dumps(query_2_5, indent=4))

menu_collection.update_many({}, {"$mul": {"price": 1.10}})
orders_collection.delete_many({"order_date": {"$lt": "2023-01-01"}})
orders_collection.update_many({"item_id": 1}, {"$inc": {"quantity": 2}})
menu_collection.delete_many({"price": {"$lt": 10}})
menu_collection.update_many({"category": "Main Course"}, {"$mul": {"price": 1.15}})

print("All queries executed and results saved.")
client.close()

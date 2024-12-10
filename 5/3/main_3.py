# Дан файл с некоторыми данными.
# Формат файла – произвольный, не совпадает с тем, что был в первом/втором заданиях.
# Необходимо считать данные и добавить их к той коллекции, куда были записаны данные в первом и втором заданиях.
# Выполните следующие запросы:
# -	удалить из коллекции документы по предикату: salary < 25 000 || salary > 175000
# -	увеличить возраст (age) всех документов на 1
# -	поднять заработную плату на 5% для произвольно выбранных профессий
# -	поднять заработную плату на 7% для произвольно выбранных городов
# -	поднять заработную плату на 10% для выборки по сложному предикату (произвольный город, произвольный набор профессий, произвольный диапазон возраста)
# -	удалить из коллекции записи по произвольному предикату

import json
from pymongo import MongoClient
from bson.json_util import dumps

file_path = 'data/task_3_item.json'
with open(file_path, 'r') as f:
    new_data = json.load(f)

client = MongoClient("mongodb://localhost:27017/")
db = client["task_database"]
collection = db["task_collection"]

collection.insert_many(new_data)
collection.delete_many({"$or": [{"salary": {"$lt": 25000}}, {"salary": {"$gt": 175000}}]})
collection.update_many({}, {"$inc": {"age": 1}})
professions = ["Программист", "Инженер", "Медсестра"]
collection.update_many({"job": {"$in": professions}}, {"$mul": {"salary": 1.05}})
cities = ["Москва", "Минск", "Санкт-Петербург"]
collection.update_many({"city": {"$in": cities}}, {"$mul": {"salary": 1.07}})
complex_filter = {
    "city": "Мадрид",
    "job": {"$in": ["Учитель", "Врач"]},
    "age": {"$gte": 30, "$lte": 50}
}
collection.update_many(complex_filter, {"$mul": {"salary": 1.10}})
random_filter = {"job": "Оператор call-центра"}
collection.delete_many(random_filter)

result = list(collection.find({}))
with open('result.json', 'w') as f:
    f.write(dumps(result, ensure_ascii=False, indent=4))

client.close()

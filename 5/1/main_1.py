# Дан файл с некоторыми данными.
# Формат файла – произвольный.
# Считайте данные из файла и запишите их в Mongo.
# Реализуйте и выполните следующие запросы:
# -	вывод* первых 10 записей, отсортированных по убыванию по полю salary;
# -	вывод первых 15 записей, отфильтрованных по предикату age < 30, отсортировать по убыванию по полю salary
# -	вывод первых 10 записей, отфильтрованных по сложному предикату: (записи только из произвольного города, записи только из трех произвольно взятых профессий), отсортировать по возрастанию по полю age
# -	вывод количества записей, получаемых в результате следующей фильтрации (age в произвольном диапазоне, year в [2019,2022], 50 000 < salary <= 75 000 || 125 000 < salary < 150 000).
# * – здесь и везде предполагаем вывод в JSON.

import pandas as pd
from pymongo import MongoClient, errors

try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    client.server_info()
except errors.ServerSelectionTimeoutError:
    print("Cannot connect to MongoDB. Ensure MongoDB is running and accessible.")
    exit()

db = client["task_database"]
collection = db["task_collection"]

file_path = 'data/task_1_item.csv'
data = pd.read_csv(file_path)

data.reset_index(inplace=True)
records = data.to_dict("records")
collection.delete_many({})
collection.insert_many(records)

query_1 = list(collection.find().sort("salary", -1).limit(10))
with open('query_1.json', 'w') as f:
    f.write(str(query_1))

query_2 = list(collection.find({"age": {"$lt": 30}}).sort("salary", -1).limit(15))
with open('query_2.json', 'w') as f:
    f.write(str(query_2))

city = "SampleCity"
professions = ["Engineer", "Doctor", "Teacher"]
query_3 = list(collection.find({"city": city, "profession": {"$in": professions}}).sort("age", 1).limit(10))
with open('query_3.json', 'w') as f:
    f.write(str(query_3))

query_4_count = collection.count_documents({
    "$and": [
        {"age": {"$gte": 25, "$lte": 35}},
        {"year": {"$gte": 2019, "$lte": 2022}},
        {
            "$or": [
                {"salary": {"$gt": 50000, "$lte": 75000}},
                {"salary": {"$gt": 125000, "$lt": 150000}}
            ]
        }
    ]
})
with open('query_4.json', 'w') as f:
    f.write(str({"count": query_4_count}))

client.close()

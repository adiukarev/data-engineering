# Дан файл с некоторыми данными.
# Формат файла – произвольный, не совпадает с тем, что был в первом задании.
# Необходимо считать данные и добавить их к той коллекции, куда были записаны данные в первом задании.
# Реализовать следующие запросы:
# -	вывод минимальной, средней, максимальной salary
# -	вывод количества данных по представленным профессиям
# -	вывод минимальной, средней, максимальной salary по городу
# -	вывод минимальной, средней, максимальной salary по профессии
# -	вывод минимального, среднего, максимального возраста по городу
# -	вывод минимального, среднего, максимального возраста по профессии
# -	вывод максимальной заработной платы при минимальном возрасте
# -	вывод минимальной заработной платы при максимальной возрасте
# -	вывод минимального, среднего, максимального возраста по городу, при условии, что заработная плата больше 50 000, отсортировать вывод по убыванию по полю avg
# -	вывод минимальной, средней, максимальной salary в произвольно заданных диапазонах по городу, профессии, и возрасту: 18<age<25 & 50<age<65
# -	произвольный запрос с $match, $group, $sort

import pandas as pd
import json
from pymongo import MongoClient

file_path = 'data/task_2_item.pkl'
new_data = pd.read_pickle(file_path)

if isinstance(new_data, list):
    new_data = pd.DataFrame(new_data)

client = MongoClient("mongodb://localhost:27017/")
db = client["task_database"]
collection = db["task_collection"]

new_data.reset_index(inplace=True)
new_records = new_data.to_dict("records")
collection.insert_many(new_records)

query_1 = list(collection.aggregate([
    {"$group": {
        "_id": None,
        "min_salary": {"$min": "$salary"},
        "avg_salary": {"$avg": "$salary"},
        "max_salary": {"$max": "$salary"}
    }}
]))
with open('query_1.json', 'w') as f:
    json.dump(query_1, f)

query_2 = list(collection.aggregate([
    {"$group": {
        "_id": "$profession",
        "count": {"$sum": 1}
    }}
]))
with open('query_2.json', 'w') as f:
    json.dump(query_2, f)

query_3 = list(collection.aggregate([
    {"$group": {
        "_id": "$city",
        "min_salary": {"$min": "$salary"},
        "avg_salary": {"$avg": "$salary"},
        "max_salary": {"$max": "$salary"}
    }}
]))
with open('query_3.json', 'w') as f:
    json.dump(query_3, f)

query_4 = list(collection.aggregate([
    {"$group": {
        "_id": "$profession",
        "min_salary": {"$min": "$salary"},
        "avg_salary": {"$avg": "$salary"},
        "max_salary": {"$max": "$salary"}
    }}
]))
with open('query_4.json', 'w') as f:
    json.dump(query_4, f)

query_5 = list(collection.aggregate([
    {"$group": {
        "_id": "$city",
        "min_age": {"$min": "$age"},
        "avg_age": {"$avg": "$age"},
        "max_age": {"$max": "$age"}
    }}
]))
with open('query_5.json', 'w') as f:
    json.dump(query_5, f)

query_6 = list(collection.aggregate([
    {"$group": {
        "_id": "$profession",
        "min_age": {"$min": "$age"},
        "avg_age": {"$avg": "$age"},
        "max_age": {"$max": "$age"}
    }}
]))
with open('query_6.json', 'w') as f:
    json.dump(query_6, f)

query_7 = list(collection.aggregate([
    {"$group": {
        "_id": "$age",
        "max_salary": {"$max": "$salary"}
    }},
    {"$sort": {"_id": 1}},
    {"$limit": 1}
]))
with open('query_7.json', 'w') as f:
    json.dump(query_7, f)

query_8 = list(collection.aggregate([
    {"$group": {
        "_id": "$age",
        "min_salary": {"$min": "$salary"}
    }},
    {"$sort": {"_id": -1}},
    {"$limit": 1}
]))
with open('query_8.json', 'w') as f:
    json.dump(query_8, f)

query_9 = list(collection.aggregate([
    {"$match": {"salary": {"$gt": 50000}}},
    {"$group": {
        "_id": "$city",
        "min_age": {"$min": "$age"},
        "avg_age": {"$avg": "$age"},
        "max_age": {"$max": "$age"}
    }},
    {"$sort": {"avg_age": -1}}
]))
with open('query_9.json', 'w') as f:
    json.dump(query_9, f)

query_10 = list(collection.aggregate([
    {"$match": {
        "$or": [
            {"age": {"$gt": 18, "$lt": 25}},
            {"age": {"$gt": 50, "$lt": 65}}
        ]
    }},
    {"$group": {
        "_id": {"city": "$city", "profession": "$profession"},
        "min_salary": {"$min": "$salary"},
        "avg_salary": {"$avg": "$salary"},
        "max_salary": {"$max": "$salary"}
    }}
]))
with open('query_10.json', 'w') as f:
    json.dump(query_10, f)

query_11 = list(collection.aggregate([
    {"$match": {"city": "SampleCity"}},
    {"$group": {
        "_id": "$profession",
        "total_salary": {"$sum": "$salary"}
    }},
    {"$sort": {"total_salary": -1}}
]))
with open('query_11.json', 'w') as f:
    json.dump(query_11, f)

client.close()

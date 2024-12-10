import json
import pandas as pd
import random
from faker import Faker
from pymongo import MongoClient

def generate_menu_data(filename):
    fake = Faker()
    categories = ["Main Course", "Appetizer", "Dessert", "Beverage"]
    menu = []
    for item_id in range(1, 21):
        menu.append({
            "item_id": item_id,
            "name": fake.word().capitalize(),
            "price": round(random.uniform(5, 50), 2),
            "category": random.choice(categories)
        })
    with open(filename, "w") as f:
        json.dump(menu, f, indent=4)

def generate_orders_data(filename):
    fake = Faker()
    orders = []
    for order_id in range(1, 51):
        orders.append({
            "order_id": order_id,
            "customer_name": fake.name(),
            "item_id": random.randint(1, 20),
            "quantity": random.randint(1, 5),
            "order_date": fake.date_between(start_date="-1y", end_date="today").isoformat()
        })
    df = pd.DataFrame(orders)
    df.to_csv(filename, index=False)

def load_data_to_mongo(menu_file, orders_file):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["restaurant"]
    menu_collection = db["menu"]
    orders_collection = db["orders"]

    with open(menu_file, "r") as f:
        menu_data = json.load(f)
    menu_collection.insert_many(menu_data)

    orders_data = pd.read_csv(orders_file).to_dict("records")
    orders_collection.insert_many(orders_data)

    client.close()

generate_menu_data("menu.json")
generate_orders_data("orders.csv")
load_data_to_mongo("menu.json", "orders.csv")

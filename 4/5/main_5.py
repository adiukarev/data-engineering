# Самостоятельно выбрать предметную область.
# Подобрать пару наборов данных разных форматов.
# Создать базу данных минимум на три таблицы.
# Заполнение данных осуществляем из файлов.
# Реализовать выполнение 6-7 запросов к базе данных с выводом результатов в json.
#
# Среди них могут быть:
# -	выборка с простым условием + сортировка + ограничение количество
# -	подсчет объектов по условию, а также другие функции агрегации
# -	группировка
# -	обновление данных
#
# В решении необходимо указать:
# -	название и описание предметной области (осмысленное)
# -	SQL для создания таблиц
# -	файлы исходных данных (можно обрезать до такого размера, чтобы влезли в GitHub)
# -	скрипт для инициализации базы данных (создание таблиц)
# -	скрипт для загрузки данных из файлов в базу данных
# -	файл базы данных
# -	скрипт с выполнением запросов к базе данных

from faker import Faker
import random
import json
import csv
import sqlite3
import pandas as pd

def initializeDatabase():
    conn = sqlite3.connect('online_store.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL,
        category TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        city TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        order_date TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
    ''')

    conn.commit()
    conn.close()

def loadData():
    conn = sqlite3.connect('online_store.db')

    with open('products.json', 'r') as f:
        products = json.load(f)
    products_df = pd.DataFrame(products)
    products_df.to_sql('products', conn, if_exists='replace', index=False)

    customers_df = pd.read_csv('customers.csv')
    customers_df.to_sql('customers', conn, if_exists='replace', index=False)

    orders_df = pd.read_csv('orders.tsv', sep='\t')
    orders_df.to_sql('orders', conn, if_exists='replace', index=False)

    conn.commit()
    conn.close()

def executeTask():
    conn = sqlite3.connect('online_store.db')

    query_1 = '''
    SELECT * FROM products
    WHERE stock > 0
    ORDER BY price ASC
    LIMIT 10
    '''
    result_1 = pd.read_sql_query(query_1, conn)
    result_1.to_json('query_1.json', orient='records')

    query_2 = '''
    SELECT category, COUNT(*) AS product_count
    FROM products
    GROUP BY category
    '''
    result_2 = pd.read_sql_query(query_2, conn)
    result_2.to_json('query_2.json', orient='records')

    query_3 = '''
    SELECT p.name, SUM(o.quantity * p.price) AS total_revenue
    FROM orders o
    JOIN products p ON o.product_id = p.id
    GROUP BY p.name
    '''
    result_3 = pd.read_sql_query(query_3, conn)
    result_3.to_json('query_3.json', orient='records')

    query_4 = '''
    SELECT c.name, AVG(o.quantity) AS avg_order_size
    FROM orders o
    JOIN customers c ON o.customer_id = c.id
    GROUP BY c.name
    '''
    result_4 = pd.read_sql_query(query_4, conn)
    result_4.to_json('query_4.json', orient='records')

    query_5 = '''
    UPDATE products
    SET stock = stock - (
        SELECT SUM(o.quantity)
        FROM orders o
        WHERE o.product_id = products.id
    )
    WHERE id IN (SELECT DISTINCT product_id FROM orders)
    '''
    cursor = conn.cursor()
    cursor.execute(query_5)
    conn.commit()

    query_6 = '''
    SELECT c.name, COUNT(o.id) AS order_count
    FROM orders o
    JOIN customers c ON o.customer_id = c.id
    GROUP BY c.name
    HAVING order_count > 3
    '''
    result_6 = pd.read_sql_query(query_6, conn)
    result_6.to_json('query_6.json', orient='records')

    conn.close()

def generateData():
    fake = Faker()

    products = []
    for i in range(1, 11):
        products.append({
            "id": i,
            "name": fake.word(),
            "price": round(random.uniform(10, 1000), 2),
            "stock": random.randint(0, 50),
            "category": fake.word()
        })
    with open('products.json', 'w') as f:
        json.dump(products, f)

    with open('customers.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'name', 'email', 'city'])
        for i in range(1, 11):
            writer.writerow([i, fake.name(), fake.email(), fake.city()])

    with open('orders.tsv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['id', 'customer_id', 'product_id', 'quantity', 'order_date'])
        for i in range(1, 21):
            writer.writerow([
                i,
                random.randint(1, 10),
                random.randint(1, 10),
                random.randint(1, 5),
                fake.date_this_year()
            ])

generateData()
initializeDatabase()
loadData()
executeTask()


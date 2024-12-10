# Дан набор файлов.
# В одних содержится информация о некоторых товарах, которые нужно сохранить в соответствующей таблице базы данных.
# В других (начинающихся с префикса upd) содержится информация об изменениях,
# которые могут задаваться разными командами: изменение цены, изменение остатков, снять/возврат продажи, удаление из каталога (таблицы).
# По одному товару могут быть несколько изменений, поэтому при создании таблицы необходимо предусмотреть поле-счетчик,
# которое инкрементируется каждый раз, когда происходит обновление строки.
# Все изменения необходимо производить, используя транзакции, проверяя изменения на корректность (например, цена или остатки после обновления не могут быть отрицательными)
# После записи всех данные и применения обновлений необходимо выполнить следующие запросы:
# -	вывести топ-10 самых обновляемых товаров
# -	проанализировать цены товаров, найдя (сумму, мин, макс, среднее) для каждой группы, а также количество товаров в группе
# -	проанализировать остатки товаров, найдя (сумму, мин, макс, среднее) для каждой группы товаров
# -	произвольный запрос

import sqlite3
import pandas as pd
import json
from IPython.display import display

product_file_path = 'data/_product_data.json'
update_file_path = 'data/_update_data.text'

with open(product_file_path, 'r') as f:
    product_data = json.load(f)

with open(update_file_path, 'r') as f:
    update_data = f.read().split("=====\n")

product_df = pd.DataFrame(product_data)

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE products (
    name TEXT,
    price REAL,
    quantity INTEGER,
    category TEXT,
    fromCity TEXT,
    isAvailable BOOLEAN,
    views INTEGER,
    update_count INTEGER DEFAULT 0
)
''')

product_df.to_sql('products', conn, if_exists='append', index=False)

for update in update_data:
    lines = update.strip().split('\n')
    if len(lines) < 3:
        continue
    name = lines[0].split('::')[1]
    method = lines[1].split('::')[1]
    param = lines[2].split('::')[1]
    try:
        cursor.execute("BEGIN TRANSACTION")
        if method == "price_abs":
            cursor.execute("UPDATE products SET price = price + ?, update_count = update_count + 1 WHERE name = ?", (float(param), name))
        elif method == "price_percent":
            cursor.execute("UPDATE products SET price = price * (1 + ?), update_count = update_count + 1 WHERE name = ?", (float(param), name))
        elif method == "quantity_add":
            cursor.execute("UPDATE products SET quantity = quantity + ?, update_count = update_count + 1 WHERE name = ?", (int(param), name))
        elif method == "quantity_sub":
            cursor.execute("UPDATE products SET quantity = quantity - ?, update_count = update_count + 1 WHERE name = ?", (int(param), name))
        elif method == "available":
            cursor.execute("UPDATE products SET isAvailable = ?, update_count = update_count + 1 WHERE name = ?", (param.lower() == 'true', name))
        elif method == "remove":
            cursor.execute("DELETE FROM products WHERE name = ?", (name,))
        cursor.execute("COMMIT")
    except Exception:
        cursor.execute("ROLLBACK")

query_1 = '''
SELECT name, update_count FROM products
ORDER BY update_count DESC
LIMIT 10
'''
result_1 = pd.read_sql_query(query_1, conn)

query_2 = '''
SELECT category,
       SUM(price) AS sum_price,
       MIN(price) AS min_price,
       MAX(price) AS max_price,
       AVG(price) AS avg_price,
       COUNT(name) AS product_count
FROM products
GROUP BY category
'''
result_2 = pd.read_sql_query(query_2, conn)

query_3 = '''
SELECT category,
       SUM(quantity) AS sum_quantity,
       MIN(quantity) AS min_quantity,
       MAX(quantity) AS max_quantity,
       AVG(quantity) AS avg_quantity
FROM products
GROUP BY category
'''
result_3 = pd.read_sql_query(query_3, conn)

query_4 = '''
SELECT category, name, MAX(views) AS max_views
FROM products
GROUP BY category
'''
result_4 = pd.read_sql_query(query_4, conn)

conn.close()

display(result_4)


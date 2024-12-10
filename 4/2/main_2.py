# Дан файл с некоторыми данными. Формат файла – произвольный.
# Данные некоторым образом связаны с теми, что были добавлены в первом задании.
# Необходимо проанализировать и установить связь между таблицами.
# Создать таблицу и наполнить ее прочитанными данными из файла.
# Реализовать и выполнить 3 запроса, где используется связь между таблицами.

import sqlite3
import pandas as pd
from IPython.display import display

pkl_path = 'data/item.pkl'
json_path = 'data/subitem.json'
pkl_data = pd.read_pickle(pkl_path)
json_data = pd.read_json(json_path)
pkl_df = pd.DataFrame(pkl_data)

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE main_items (
    id INTEGER,
    name TEXT,
    street TEXT,
    city TEXT,
    zipcode INTEGER,
    floors INTEGER,
    year INTEGER,
    parking BOOLEAN,
    prob_price REAL,
    views INTEGER
)
''')
pkl_df.to_sql('main_items', conn, if_exists='append', index=False)

cursor.execute('''
CREATE TABLE sub_items (
    name TEXT,
    rating REAL,
    convenience INTEGER,
    security INTEGER,
    functionality INTEGER,
    comment TEXT
)
''')
json_data.to_sql('sub_items', conn, if_exists='append', index=False)

query_1 = '''
SELECT m.name, m.city, s.rating, s.comment
FROM main_items m
JOIN sub_items s ON m.name = s.name
'''
result_1 = pd.read_sql_query(query_1, conn)

query_2 = '''
SELECT m.city, COUNT(*) AS high_rating_count
FROM main_items m
JOIN sub_items s ON m.name = s.name
WHERE s.rating > 4.0
GROUP BY m.city
'''
result_2 = pd.read_sql_query(query_2, conn)

query_3 = '''
SELECT m.city, AVG(s.rating) AS avg_rating, SUM(m.views) AS total_views
FROM main_items m
JOIN sub_items s ON m.name = s.name
GROUP BY m.city
'''
result_3 = pd.read_sql_query(query_3, conn)

conn.close()

display(result_3)
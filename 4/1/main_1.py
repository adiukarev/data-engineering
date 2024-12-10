# Дан файл с некоторыми данными. Формат файла – произвольный.
# Спроектируйте на его основе и создайте таблицу в базе данных (SQLite).
# Считайте данные из файла и запишите их в созданную таблицу.
# Реализуйте и выполните следующие запросы:
# - вывод первых (VAR+10) отсортированных по произвольному числовому полю строк из таблицы в файл формата json;
# - вывод (сумму, мин, макс, среднее) по произвольному числовому полю;
# -	вывод частоты встречаемости для категориального поля;
# -	вывод первых (VAR+10) отфильтрованных по произвольному предикату отсортированных по произвольному числовому полю строк из таблицы в файл формате json.

import sqlite3
import pandas as pd

file_path = 'data/subitem.json'
data = pd.read_json(file_path)

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE items (
    name TEXT,
    rating REAL,
    convenience INTEGER,
    security INTEGER,
    functionality INTEGER,
    comment TEXT
)
''')

data.to_sql('items', conn, if_exists='append', index=False)

VAR = 5
query_1 = f"SELECT * FROM items ORDER BY rating LIMIT {VAR + 10}"
result_1 = pd.read_sql_query(query_1, conn)
result_1.to_json('query_1.json', orient='records')

query_2 = '''
SELECT
    SUM(rating) AS sum,
    MIN(rating) AS min,
    MAX(rating) AS max,
    AVG(rating) AS avg
FROM items
'''
result_2 = pd.read_sql_query(query_2, conn)
result_2.to_json('query_2.json', orient='records')

query_3 = '''
SELECT name, COUNT(*) AS frequency
FROM items
GROUP BY name
'''
result_3 = pd.read_sql_query(query_3, conn)
result_3.to_json('query_3.json', orient='records')

query_4 = f'''
SELECT * FROM items
WHERE security > 3
ORDER BY rating DESC
LIMIT {VAR + 10}
'''
result_4 = pd.read_sql_query(query_4, conn)
result_4.to_json('query_4.json', orient='records')

conn.close()

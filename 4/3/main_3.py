# Дано два файла разных форматов.
# Необходимо проанализировать их структуру и выделить общие хранимые данные.
# Необходимо создать таблицу для хранения данных в базе данных.
# Произведите запись данных из файлов разных форматов в одну таблицу.
# Реализуйте и выполните следующие запросы:
# -	вывод первых (VAR+10) отсортированных по произвольному числовому полю строк из таблицы в файл формата json;
# -	вывод (сумму, мин, макс, среднее) по произвольному числовому полю;
# -	вывод частоты встречаемости для категориального поля;
# -	вывод первых (VAR+15) отфильтрованных по произвольному предикату отсортированных по произвольному числовому полю строк из таблицы в файл формате json.

import sqlite3
import pandas as pd
import msgpack

csv_path = 'data/_part_1.csv'
msgpack_path = 'data/_part_2.msgpack'

csv_data = pd.read_csv(csv_path, sep=';', on_bad_lines='skip')
with open(msgpack_path, 'rb') as f:
    msgpack_data = msgpack.unpack(f, raw=False)
msgpack_df = pd.DataFrame(msgpack_data)

common_columns = set(csv_data.columns).intersection(set(msgpack_df.columns))
common_data_csv = csv_data[list(common_columns)]
common_data_msgpack = msgpack_df[list(common_columns)]
combined_data = pd.concat([common_data_csv, common_data_msgpack], ignore_index=True)

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()
table_schema = ', '.join([f"{col} TEXT" for col in combined_data.columns])
cursor.execute(f"CREATE TABLE combined_table ({table_schema})")
combined_data.to_sql('combined_table', conn, if_exists='append', index=False)

VAR = 5

query_1 = f'''
SELECT * FROM combined_table
ORDER BY duration_ms
LIMIT {VAR + 10}
'''
result_1 = pd.read_sql_query(query_1, conn)
result_1.to_json('query_1.json', orient='records')

query_2 = '''
SELECT SUM(CAST(duration_ms AS REAL)) AS total,
       MIN(CAST(duration_ms AS REAL)) AS minimum,
       MAX(CAST(duration_ms AS REAL)) AS maximum,
       AVG(CAST(duration_ms AS REAL)) AS average
FROM combined_table
'''
result_2 = pd.read_sql_query(query_2, conn)
result_2.to_json('query_2.json', orient='records')


query_3 = '''
SELECT artist, COUNT(*) AS frequency
FROM combined_table
GROUP BY artist
'''
result_3 = pd.read_sql_query(query_3, conn)
result_3.to_json('query_3.json', orient='records')

query_4 = f'''
SELECT * FROM combined_table
WHERE CAST(duration_ms AS REAL) > 200000
ORDER BY duration_ms DESC
LIMIT {VAR + 15}
'''
result_4 = pd.read_sql_query(query_4, conn)
result_4.to_json('query_4.json', orient='records')

conn.close()

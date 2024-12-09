# Исследовать структуру html-файлов, чтобы произвести парсинг всех данных.
# В каждом файле содержится информация об одном или нескольких объектах из случайной предметной области.
# Перечень всех характеристик объекта может меняться (у отдельного объекта могут отсутствовать некоторые характеристики).
# Полученные данные собрать и записать в json. Выполните также ряд операций с данными:
# - отсортируйте значения по одному из доступных полей
# - выполните фильтрацию по другому полю (запишите результат отдельно)
# - для одного выбранного числового поля посчитайте статистические характеристики (сумма, мин/макс, среднее и т.д.)
# - для одного текстового поля посчитайте частоту меток

import os
from bs4 import BeautifulSoup
import json
from collections import Counter

folder_path = './data'
file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.html')]

def extract_products_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        products = []
        for item in soup.select('.product-item'):
            product = {}
            product['id'] = item.select_one('a.add-to-favorite').get('data-id', None)
            product['name'] = item.select_one('span').text.strip() if item.select_one('span') else None
            product['price'] = int(item.select_one('price').text.strip().replace('₽', '').replace(' ', '')) if item.select_one('price') else None
            product['bonuses'] = int(item.select_one('strong').text.strip().replace('+ начислим ', '').replace(' бонусов', '')) if item.select_one('strong') else None
            details = {}
            for li in item.select('ul li'):
                detail_type = li.get('type', '').strip()
                details[detail_type] = li.text.strip()
            product['details'] = details
            products.append(product)
        return products

all_products = []
for file_path in file_paths:
    all_products.extend(extract_products_from_html(file_path))

output_json_path = 'products.json'
with open(output_json_path, 'w', encoding='utf-8') as json_file:
    json.dump(all_products, json_file, ensure_ascii=False, indent=4)

sorted_products = sorted(all_products, key=lambda x: x['price'] if x['price'] else 0)
filtered_products = [product for product in all_products if product['bonuses'] and product['bonuses'] > 1000]
prices = [product['price'] for product in all_products if product['price']]
price_stats = {'sum': sum(prices), 'min': min(prices), 'max': max(prices), 'average': sum(prices) / len(prices)}
matrix_types = [product['details'].get('matrix', '') for product in all_products if 'matrix' in product['details']]
matrix_frequency = Counter(matrix_types)

print("Sorted Products by Price:")
print(sorted_products[:5])
print("\nFiltered Products with Bonuses > 1000:")
print(filtered_products[:5])
print("\nPrice Statistics:")
print(price_stats)
print("\nMatrix Type Frequency:")
print(matrix_frequency)

# Исследовать структуру xml-файлов, чтобы произвести парсинг всех данных.
# В каждом файле содержится информация об одном или нескольких объектах из случайной предметной области.
# Перечень всех характеристик объекта может меняться (у отдельного объекта могут отсутствовать некоторые характеристики).
# Полученные данные собрать и записать в json. Выполните также ряд операций с данными:
# - отсортируйте значения по одному из доступных полей
# - выполните фильтрацию по другому полю (запишите результат отдельно)
# - для одного выбранного числового поля посчитайте статистические характеристики (сумма, мин/макс, среднее и т.д.)
# - для одного текстового поля посчитайте частоту меток

import os
import xml.etree.ElementTree as ET
import json
from collections import Counter

folder_path = './data'
file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.xml')]

def extract_data_from_xml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        tree = ET.parse(file)
        root = tree.getroot()
        items = []
        for item in root.findall('clothing'):
            data = {child.tag: child.text.strip() for child in item}
            items.append(data)
        return items

all_data = []
for file_path in file_paths:
    all_data.extend(extract_data_from_xml(file_path))

output_json_path = 'clothing_data.json'
with open(output_json_path, 'w', encoding='utf-8') as json_file:
    json.dump(all_data, json_file, ensure_ascii=False, indent=4)

sorted_data = sorted(all_data, key=lambda x: int(x['price']) if 'price' in x else 0)
filtered_data = [item for item in all_data if 'color' in item and item['color'] == 'Синий']
prices = [int(item['price']) for item in all_data if 'price' in item]
price_stats = {'sum': sum(prices), 'min': min(prices), 'max': max(prices), 'average': sum(prices) / len(prices) if prices else 0}
categories = [item['category'] for item in all_data if 'category' in item]
category_frequency = Counter(categories)

print("Отсортированные данные по цене:")
print(sorted_data[:5])
print("\nОтфильтрованные данные (цвет 'Синий'):")
print(filtered_data[:5])
print("\nСтатистика по цене:")
print(price_stats)
print("\nЧастота категорий:")
print(category_frequency)

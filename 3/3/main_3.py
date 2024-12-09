# Исследовать структуру xml-файлов, чтобы произвести парсинг всех данных.
# В каждом файле содержится информация об одном объекте из случайной предметной области.
# Полученные данные собрать и записать в json. Выполните также ряд операций с данными:
# - отсортируйте значения по одному из доступных полей
# - выполните фильтрацию по другому полю (запишите результат отдельно)
# -для одного выбранного числового поля посчитайте статистические характеристики (сумма, мин/макс, среднее и т.д.)
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
        return {child.tag: child.text.strip() for child in root}

all_data = [extract_data_from_xml(file_path) for file_path in file_paths]

output_json_path = 'stars.json'
with open(output_json_path, 'w', encoding='utf-8') as json_file:
    json.dump(all_data, json_file, ensure_ascii=False, indent=4)

sorted_data = sorted(all_data, key=lambda x: int(x['radius']) if 'radius' in x else 0)
filtered_data = [entry for entry in all_data if 'constellation' in entry and entry['constellation'] == 'Овен']
radii = [int(entry['radius']) for entry in all_data if 'radius' in entry]
radius_stats = {'sum': sum(radii), 'min': min(radii), 'max': max(radii), 'average': sum(radii) / len(radii) if radii else 0}
spectral_classes = [entry['spectral-class'] for entry in all_data if 'spectral-class' in entry]
spectral_frequency = Counter(spectral_classes)

print("Отсортированные данные по радиусу:")
print(sorted_data[:5])
print("\nОтфильтрованные данные для созвездия 'Овен':")
print(filtered_data[:5])
print("\nСтатистика по радиусу:")
print(radius_stats)
print("\nЧастота спектральных классов:")
print(spectral_frequency)

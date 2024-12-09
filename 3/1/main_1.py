# Исследовать структуру html-файлов, чтобы произвести парсинг всех данных.
# В каждом файле содержится информация об одном объекте из случайной предметной области.
# Полученные данные собрать и записать в json. Выполните также ряд операций с данными:
# - отсортируйте значения по одному из доступных полей
# - выполните фильтрацию по другому полю (запишите результат отдельно)
# - для одного выбранного числового поля посчитайте статистические характеристики (сумма, мин/макс, среднее и т.д.)
# - для одного текстового поля посчитайте частоту меток

import os
import json
from bs4 import BeautifulSoup
import pandas as pd

def parse_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    city = soup.find('span').text.split(":")[1].strip()
    building = soup.find('h1', class_='title').text.split(":")[1].strip()
    street, postal_code = soup.find('p', class_='address-p').text.split("Индекс:")
    street = street.split(":")[1].strip()
    postal_code = postal_code.strip()

    floors = soup.find('span', class_='floors')
    floors = int(floors.text.split(":")[1].strip()) if floors else None

    year = soup.find('span', class_='year')
    if year:
        year_text = year.text.split(":")
        year = int(year_text[1].strip()) if len(year_text) > 1 else None
    else:
        year = None

    parking = soup.find('span', string=lambda text: text and "Парковка" in text)
    parking = parking.string.split(":")[1].strip() if parking else None

    rating = float(soup.find('span', string=lambda text: text and "Рейтинг" in text).string.split(":")[1].strip())
    views = int(soup.find('span', string=lambda text: text and "Просмотры" in text).string.split(":")[1].strip())

    return {
        "city": city,
        "building": building,
        "street": street,
        "postal_code": postal_code,
        "floors": floors,
        "year": year,
        "parking": parking,
        "rating": rating,
        "views": views
    }

data_folder = 'data'
data = []

for file_name in os.listdir(data_folder):
    if file_name.endswith(".html"):
        data.append(parse_html(os.path.join(data_folder, file_name)))

json_data = json.dumps(data, ensure_ascii=False, indent=4)

sorted_data = sorted(data, key=lambda x: x['rating'], reverse=True)

filtered_data = [item for item in data if item['parking'] == 'есть']

rating_series = pd.Series([item['rating'] for item in data])
rating_stats = {
    "sum": rating_series.sum(),
    "min": rating_series.min(),
    "max": rating_series.max(),
    "mean": rating_series.mean()
}

city_series = pd.Series([item['city'] for item in data])
city_freq = city_series.value_counts().to_dict()

with open('sorted_data.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_data, f, ensure_ascii=False, indent=4)

with open('filtered_data.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=4)

with open('rating_stats.json', 'w', encoding='utf-8') as f:
    json.dump(rating_stats, f, ensure_ascii=False, indent=4)

with open('city_frequency.json', 'w', encoding='utf-8') as f:
    json.dump(city_freq, f, ensure_ascii=False, indent=4)

print("Sorted Data (by rating): sorted_data.json")
print("Filtered Data (parking available): filtered_data.json")
print("Rating Stats: rating_stats.json")
print("City Frequency: city_frequency.json")

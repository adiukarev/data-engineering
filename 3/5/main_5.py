# Самостоятельно найти сайт, соответствующий следующим условиям:
# - непопулярный, регионального уровня или из узкой области (с целью избежать дублирования);
# - наличие страниц-каталогов, где есть информация сразу по нескольких объектам;
# - наличие страниц, посвященных отдельному объекту.
#
# Необходимо:
# - спарсить нескольких страниц (минимум 10), посвященных только одному объекту;
# - спарсить страницы-каталоги, где размещена информация сразу по нескольким объектам.
#
# Данные можно скачать и сохранить локально в виде html, а можно организовать их получение напрямую через обращение к серверу сайта.
# Результаты парсинга собрать отдельно по каждой подзадаче и записать в отдельный json.
# Выполните произвольные операции с данными:
# - отсортируйте значения по одному из доступных полей;
# - выполните фильтрацию по другому полю (запишите результат отдельно);
# - для одного выбранного числового поля посчитайте показатели статистики;
# - для одного текстового поля посчитайте частоту меток.

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
from collections import Counter
import statistics

catalog_url = "https://xn--80aacacvtbthqmh0dxl.xn--p1ai/catalog/"
driver = webdriver.Chrome()

def parse_catalog_page(url):
    driver.get(url)
    time.sleep(3)
    object_links = [elem.get_attribute('href') for elem in driver.find_elements(By.CSS_SELECTOR, ".item a")]
    return object_links

def parse_object_page(url):
    driver.get(url)
    time.sleep(3)
    data = {
        "name": driver.find_element(By.TAG_NAME, "h1").text if driver.find_elements(By.TAG_NAME, "h1") else None,
        "address": driver.find_element(By.CLASS_NAME, "address").text if driver.find_elements(By.CLASS_NAME, "address") else None,
        "phone": driver.find_element(By.CLASS_NAME, "phone").text if driver.find_elements(By.CLASS_NAME, "phone") else None,
        "description": driver.find_element(By.CLASS_NAME, "description").text if driver.find_elements(By.CLASS_NAME, "description") else None,
    }
    return data

object_links = parse_catalog_page(catalog_url)
object_links = object_links[:10]
object_data = []
for link in object_links:
    object_data.append(parse_object_page(link))

with open("object_data.json", "w", encoding="utf-8") as f:
    json.dump(object_data, f, ensure_ascii=False, indent=4)

sorted_data = sorted(object_data, key=lambda x: x.get("name", ""))
filtered_data = [obj for obj in object_data if obj.get("phone")]
descriptions = [len(obj["description"]) for obj in object_data if obj.get("description")]
if descriptions:
    description_stats = {
        "sum": sum(descriptions),
        "min": min(descriptions),
        "max": max(descriptions),
        "average": statistics.mean(descriptions)
    }
else:
    description_stats = {
        "sum": 0,
        "min": 0,
        "max": 0,
        "average": 0
    }
addresses = [obj["address"] for obj in object_data if obj.get("address")]
address_frequency = Counter(addresses)

print("Отсортированные данные по названию:", sorted_data)
print("Отфильтрованные данные с телефоном:", filtered_data)
print("Статистика по длине описаний:", description_stats)
print("Частота адресов:", address_frequency)

driver.quit()

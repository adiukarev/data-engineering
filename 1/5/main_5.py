# Считайте фрагмент html из файла согласно варианту (67).
# Извлеките данные из таблицы html. Запишите полученный csv файл.

import csv
from bs4 import BeautifulSoup

with open('fifth_task.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

table = BeautifulSoup(html_content, 'html.parser').find('table', { 'id': 'product-table' })

data = list()
data.append([th.get_text(strip=True) for th in table.find_all('th')])

for row in table.find_all('tr')[1:]:
    columns = row.find_all('td')
    row_data = [col.get_text(strip=True) for col in columns]
    data.append(row_data)

with open('result_5.csv', 'w', newline='', encoding='utf-8') as result:
    writer = csv.writer(result)
    writer.writerows(data)

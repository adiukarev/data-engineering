# Считайте csv файл и выполните с ним определенные действия согласно вашему варианту (67).
# Результаты поиска значений (среднее, максимум и минимум) запишите в отдельный файл: каждое число на новой строке.
# Результаты модификаций исходного файла – в отдельный csv файл.
# Условия:
# 1. Удалите из таблицы столбец category
# 2. Найдите среднее арифметическое по столбцу quantity
# 3. Найдите максимум по столбцу quantity
# 4. Найдите минимум по столбцу rating
# 5. Отфильтруйте значения, взяв только те, quantity которых меньше 40

import csv

result_list = list()
averageQuantity = None
maxQuantity = None
minRating = None

with open('data_4.txt', newline='\n', encoding='utf-8') as data:
    data = csv.reader(data, delimiter=',')

    data_list = list()
    for row in data:
        data_list.append(row)

    quantityIndex = data_list[0].index('quantity')
    quantity_list = list()
    for row in data_list[1:]:
        quantity_list.append(int(row[quantityIndex]))

    averageQuantity = sum(quantity_list) / len(quantity_list)
    maxQuantity = max(quantity_list)

    ratingIndex = data_list[0].index('rating')
    rating_list = list()
    for row in data_list[1:]:
        rating_list.append(float(row[ratingIndex]))

    minRating = min(rating_list)

    result_list.append(data_list[0])
    for row in data_list[1:]:
        if int(row[quantityIndex]) < 40:
            result_list.append(row)

    categoryIndex = data_list[0].index('category')
    for i, item in enumerate(result_list):
        result_list[i] = [item for x, item in enumerate(result_list[i]) if x != categoryIndex]

with open(r'result_4.csv', 'w', encoding='utf-8', newline='') as result:
    writer = csv.writer(result, delimiter=',', quoting=csv.QUOTE_MINIMAL)

    for row in result_list:
        writer.writerow(row)

# Найдите набор данных (csv, json), размер которого превышает 20-30 Мб.
# Отберите для дальнейшей работы в нем 7-10 полей (пропишите это преобразование в коде).
# Для полей, представляющих числовые данные, рассчитайте характеристики:
# максимальное и минимальное значения, среднее арифметическое, сумму, стандартное отклонение.
# Для полей, представляющий текстовые данные (в виде меток некоторых категорий) рассчитайте частоту встречаемости.
# Сохраните полученные расчеты в json.
# Сохраните набор данных с помощью разных форматов: csv, json, msgpack, pkl.
# Сравните размеры полученных файлов

import csv
import json

import numpy as np
import msgpack
import pickle
import os

data_list = list()

with open('data_5.csv', 'r', newline="") as data:
    heading = next(data)

    for row in csv.reader(data):
        data_list.append(row)

YEAR = list()
MONTH = list()
SUPPLIER = list()
ITEM_CODE = list()
ITEM_DESCRIPTION = list()
ITEM_TYPE = list()
RETAIL_SALES = list()
RETAIL_TRANSFERS = list()
WAREHOUSE_SALES = list()

size = len(data_list)

full_item = list()

def execute_math_operation(item):
    max_item = float(item[0])
    min_item = float(item[0])
    avr_item = 0.0
    sum_item = 0.0
    elements = list()

    for x in item:
        max_item = max(max_item, float(x))
        min_item = min(min_item, float(x))
        sum_item += float(x)
        avr_item = round(sum_item / size)
        elements.append(float(x))

    return {
        'max_item': max_item,
        'min_item': min_item,
        'sum_item': sum_item,
        'avr_item': avr_item,
        'sigma': np.std(elements)
    }

full_coll = list()

for i in range(0, len(data_list)):
    YEAR.append(data_list[i][0])
    MONTH.append(data_list[i][1])
    SUPPLIER.append(data_list[i][2])
    ITEM_CODE.append(data_list[i][3])
    ITEM_DESCRIPTION.append(data_list[i][4])
    ITEM_TYPE.append(data_list[i][5])
    RETAIL_SALES.append(data_list[i][6])
    RETAIL_TRANSFERS.append(data_list[i][7])
    WAREHOUSE_SALES.append(data_list[i][8])

def execute_replace_item(list_elem):
    for item in range(0, len(list_elem)):
        if list_elem[item]=='BC' or list_elem[item]=='WC' or list_elem[item] == '':
            list_elem[item] = 0

    return list_elem

YEAR = execute_replace_item(YEAR)
RETAIL_SALES = execute_replace_item(RETAIL_SALES)
WAREHOUSE_SALES = execute_replace_item(WAREHOUSE_SALES)

full_YEAR = execute_math_operation(YEAR)
full_MONTH = execute_math_operation(MONTH)
full_RETAIL_SALES = execute_math_operation(RETAIL_SALES)
full_RETAIL_TRANSFERS = execute_math_operation(RETAIL_TRANSFERS)
full_WAREHOUSE_SALES = execute_math_operation(WAREHOUSE_SALES)

def execute_repeat(elem):
    dict_all = dict()
    for i in sorted(elem):
        if i in dict_all:
            dict_all[i] += 1
        else:
            dict_all[i] = 1
    dict_all = dict(sorted(dict_all.items(), reverse=True, key=lambda item: item[1]))

    return dict_all

full_SUPPLIER = execute_repeat(SUPPLIER)
full_ITEM_CODE = execute_repeat(ITEM_CODE)
full_ITEM_DESCRIPTION = execute_repeat(ITEM_DESCRIPTION)
full_ITEM_TYPE = execute_repeat(ITEM_TYPE)

data_collum = {
    'YEAR' : full_YEAR,
    'MONTH': full_MONTH,
    'SUPPLIER' : full_SUPPLIER,
    'ITEM_CODE': full_ITEM_CODE,
    'ITEM_DESCRIPTION': full_ITEM_DESCRIPTION,
    'ITEM_TYPE': full_ITEM_TYPE,
    'RETAIL_SALES': full_RETAIL_SALES,
    'RETAIL_TRANSFERS': full_RETAIL_TRANSFERS,
    'WAREHOUSE_SALES': full_WAREHOUSE_SALES
}

with open(r'result_5.json', 'w') as result:
    result.write(json.dumps(data_collum))

with open(r'data_5.json', 'w') as result:
    result.write(json.dumps(data_list))

with open(r'data_5.msgpack', 'wb') as result:
    result.write(msgpack.dumps(data_list))

with open(r'data_5.pickle', 'wb') as result:
    result.write(pickle.dumps(data_list))

print(f'data_5.csv size: {os.path.getsize("data_5.csv")}')
print(f'data_5.json size: {os.path.getsize("data_5.json")}')
print(f'data_5.msgpack size: {os.path.getsize("data_5.msgpack")}')
print(f'data_5.pickle size: {os.path.getsize("data_5.pickle")}')
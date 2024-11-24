# Загрузите матрицу из файла с форматом npy.
# Подсчитайте сумму всех элементов и их среднее арифметическое,
# подсчитайте сумму и среднее арифметическое главной и побочной диагоналей матрицы.
# Найдите максимальное и минимальное значение. Полученные значения запишите в json следующего формата:
# {
#     sum: 4,
#     avr: 4,
#     sumMD: 4, // главная диагональ
#     avrMD: 5,
#     sumSD: 4, // побочная диагональ
#     avrSD: 5,
#     max: 4,
#     min: 2
# }
#
# Исходную матрицу необходимо нормализовать и сохранить в формате npy.

import json
import numpy as np

data = np.load('data_1.npy')

data_len = len(data)
sum_res = 0
sumMD_res = 0
avrMD_res = 0
sumSD_res = 0
max_res = data[0][0]
min_res = data[0][0]
item = dict()

for i in range(0, data_len):
    for j in range(0, data_len):
        sum_res += data[i][j]

        if i == j:
            sumMD_res += data[i][j]
        elif i + j == (data_len - 1):
            sumSD_res += data[i][j]

        max_res = max(max_res, data[i][j])
        min_res = min(min_res, data[i][j])

item = {
    'sum': float(sum_res),
    'avr': float(sum_res / (data_len * data_len)),
    'sumMD': float(sumMD_res),
    'avrMD': float(sumMD_res / data_len),
    'sumSD': float(sumSD_res),
    'avrSD': float(sumSD_res / data_len),
    'max': float(max_res),
    'min': float(min_res),
}

with open('result_1_1.json', 'w') as result:
    result.write(json.dumps(item))

new_matrix = list()

for x in data:
    s_new = []

    for t in x:
        t = t / sum_res
        s_new.append(t)

    new_matrix.append(s_new)

matrix = np.array(new_matrix, dtype = float)

np.save(r'result_1_2', matrix)

print(matrix)
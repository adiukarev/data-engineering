# Считайте файл тестовый согласно вашему варианту (67).
# Тестовый файл содержит определенное количество строк, в каждой из которых расположено определенное количество чисел, разделенных пробелом.
# В каждом варианте имеются указания следующего вида:
# сначала задается операция, которую необходимо произвести для каждой строки, в результате получаем одно значение для каждой строки.
# Таким образом формируется столбец, к которому нужно применить вторую указанную операцию.
# Финальный результат записываем в текстовый файл.

# Операция в рамках одной строки: суммирование только абсолютных значений всех чисел, квадрат которых больше 100000.
# Операция для полученного столбца: сортировка столбца по убыванию, вывод топ-10 строк.

import math

with open('data_2.txt')as data:
    lines = data.readlines()

sum_lines = list()

for line in lines:
    nums = map(int, line.split())

    sum_lines.append(sum(abs(num) for num in nums if num ** 2 > 100000))

with open(r'result_2_1.txt', 'w', encoding='utf-8') as result:
    for value in sum_lines:
        result.write(str(value) + '\n')

    result.write(str(sum(sum_line for sum_line in sum_lines)))

with open(r'result_2_2.txt', 'w', encoding='utf-8') as result:
    sorted_nums = sorted(sum_lines, reverse=True)[:10]

    for sorted_num in sorted_nums:
        result.write(str(sorted_num) + '\n')
# Считайте текстовый файл согласно вашему варианту (67).
# Текстовый файл представляет собой некоторый текст произвольной длины.

# Общая часть:

# Подсчитайте частоту всех слов, встречающихся в тексте.
# В результирующем файле выведите полученные данные в порядке убывания их частоты:

with open('data_1.txt') as data:
    data = data.read()

data = sorted(data.replace('.', ' ').replace(',', ' ').replace('!', ' ').replace('?', ' ').split())
dictionary = dict()

for item in data:
    if item in dictionary:
        dictionary[item] += 1
    else:
        dictionary[item] = 1

results = (dict(sorted(dictionary.items(), reverse=True, key=lambda item: item[1])))

with open(r'result_1_1.txt', 'w', encoding='utf-8') as result:
    for key, value in results.items():
        result.write(key + ':' + str(value) + '\n')

# Подсчитайте количество предложений в каждом абзаце:

import re

with open('data_1.txt') as data:
    lines = data.readlines()

dictionary = dict()

for i, value in enumerate(lines):
    dictionary[i] = len([s for s in re.split(r'[.!?]+', value.strip()) if s.strip()])

with open(r'result_1_2.txt', 'w', encoding='utf-8') as result:
    for key, value in dictionary.items():
        result.write(str(key) + ':' + str(value) + '\n')


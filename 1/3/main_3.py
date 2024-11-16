# Считайте файл согласно вашему варианту (67).
# В строках имеются пропуски, обозначенные «NA» – замените их, рассчитав среднее значение соседних чисел.
# Проведите фильтрацию данных в рамках каждой строки тем способом, который соответствует вашему варианту, а также результирующую операцию и ее вывод в текстовый файл.
# Условие фильтрации: Оставляем положительные значения, квадрат которых не превышает 2500.
# Формат вывода: Среднее по каждой строке

with open('data_3.txt') as data:
    lines = data.readlines()

new_list = list()

for line in lines:
    items = line.replace('\n','').split(' ')

    for x in range(1, len(items) - 1):
        if items[x] == 'N/A':
            prev_item = int(items[x - 1]) if x - 1 >= 0 else 0
            next_item = int(items[x + 1]) if x + 1 < len(items) else 0

            items[x] = (prev_item + next_item) / 2

    filter_list = list()

    for i in items:
        float_num = float(i)

        if (float_num < 0):
            continue

        if float_num ** 2 <= 2500:
            filter_list.append(int(float_num))

    new_list.append(filter_list)

with open(r'result_3.txt', 'w', encoding='utf-8') as result:
    for row in new_list:
        if (len(row) > 0):
            result.write(str(sum(row) / len(row)) + '\n')
        else:
            result.write('0' + '\n')
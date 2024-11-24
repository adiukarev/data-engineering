# Считайте массив объектов в формате json.
# Агрегируйте информацию по каждому товару, получив следующую информацию:
# средняя цена, максимальная цена, минимальная цена.
# Сохранить полученную информацию по каждому объекту в формате json, а также в формате msgpack.
# Сравните размеры полученных файлов.

import json
import msgpack
import os

with open('data_3.json') as data:
    data = json.load(data)

    products = {}

    for item in data:
        if item['name'] in products:
            products[item['name']].append(item['price'])
        else:
            products[item['name']] = list()
            products[item['name']].append(item['price'])

    result = list()

    for name, prices in products.items():
        sum_price = 0
        min_price = prices[0]
        max_price = prices[0]

        for price in prices:
            sum_price += price
            min_price = min(min_price, price)
            max_price = max(max_price, price)

        result.append({
            'name': name,
            'avr': sum_price / len(prices),
            'max': max_price,
            'min': min_price,
            'sum': sum_price,
        })

    with open(r'result_3.json', 'w') as file_result:
        file_result.write(json.dumps(result))

    with open(r'result_3.msgpack', 'wb') as file_msgpack:
        file_msgpack.write(msgpack.dumps(result))

result_3_json_size = os.path.getsize("result_3.json")
result_3_msgpack_size = os.path.getsize("result_3.msgpack")

print(f'result_3_json size: {result_3_json_size}')
print(f'result_3_msgpack size: {result_3_msgpack_size}')
print(f'Difference in size between files: {result_3_json_size - result_3_msgpack_size}')
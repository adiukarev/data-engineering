# Считайте данные в формате pkl о товарах.
# Также считайте данные из файла формата json о новых ценах для каждого товара:
# {
#     name: "Apple",
#     method: "add"|"sub"|"percent+"|"percent-",
#     param: 4|0.01
# }
# Обновите цены для товаров в зависимости от метода:
# "add" – добавить значение param к цене;
# "sub" – отнять значение param от цены;
# "percent+" – поднять на param % (1% = 0.01);
# "percent-" – снизить на param %.
# Сохраните модифицированные данные обратно в формат pkl.

import json
import pickle

def update_price(price, param):
    method = param["method"]

    if method == 'add':
        price['price'] += param['param']
    elif method == 'sub':
        price['price'] -= param['param']
    elif method == 'percent+':
        price['price'] += (price['price'] * param['param'])
    elif method == 'percent-':
        price['price'] -= (price['price'] * param['param'])

    price['price'] = round(price["price"], 2)


with open('data_4_products.pkl', 'rb') as result:
    data_pkl = pickle.load(result)

with open('data_4_updates.json') as result:
    data_json = json.load(result)

products = dict()

for item in data_json:
    products[item['name']] = item

print(products)

for item in data_pkl:
    x = products[item['name']]
    update_price(item, x)

with open(r'result_4.pkl', 'wb') as result:
    result.write(pickle.dumps(data_pkl))
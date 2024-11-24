# Загрузите матрицу из файла с форматом npy.
# Создайте три массива x, y, z.
# Отберите из матрицы значения, которые превышают следующее значение: (500 + 67 (вариант) = 567),
# следующим образом: индексы элемента разнесите по массивам x, y, а само значение в массив z.
# Сохраните полученные массив в файла формата npz.
# Воспользуйтесь методами np.savez() и np.savez_compressed().
# Сравните размеры полученных файлов.

import os.path

import numpy as np

data = np.load('data_2.npy')
x = list()
y = list()
z = list()
data_len = len(data)

variant = 67

for i in range(0, data_len):
    for j in range(0, data_len):
        if data[i][j] > 500 + variant:
            x.append(i)
            y.append(j)
            z.append(data[i][j])

np.savez(r'result_2', x=x, y=y, z=z)
np.savez_compressed(r'result_2_compressed', x=x, y=y, z=z)

result_2_size = os.path.getsize("result_2.npz")
result_2_compressed_size = os.path.getsize("result_2_compressed.npz")

print(f'result_2 size: {result_2_size}')
print(f'result_2_compressed size: {result_2_compressed_size}')
print(f'Difference in size between files: {result_2_size - result_2_compressed_size}')
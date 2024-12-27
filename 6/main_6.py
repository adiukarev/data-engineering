import pandas as pd
import matplotlib.pyplot as plt
import json
import os

# Задача 1: Загрузка данных
file_path = "flights.csv"  # https://www.kaggle.com/datasets/usdot/flight-delays?select=flights.csv
chunk_size = 500000

sample_data = pd.read_csv(file_path, nrows=chunk_size, low_memory=False)

# Задача 2: Анализ объема данных
# a. Объем памяти файла на диске
file_size = os.path.getsize(file_path) / (1024 ** 2)  # МБ
print(f"Размер файла на диске: {file_size:.2f} МБ")

# b. Объем памяти набора данных в оперативной памяти
data_memory = sample_data.memory_usage(deep=True).sum() / (1024 ** 2)
print(f"Объем памяти набора данных в памяти: {data_memory:.2f} МБ")

# c. Анализ памяти для каждой колонки
column_memory = sample_data.memory_usage(deep=True).loc[sample_data.columns]
column_memory_percentage = (column_memory / column_memory.sum()) * 100
dtype_info = sample_data.dtypes

column_stats = pd.DataFrame({
    "Column": column_memory.index,
    "Memory_MB": column_memory.values,
    "Memory_Percentage": column_memory_percentage.values,
    "Dtype": dtype_info.astype(str).values
})

# Сортировка данных по памяти
column_stats_sorted = column_stats.sort_values(by="Memory_MB", ascending=False)
column_stats_sorted.to_json("column_stats_unoptimized.json", orient="records")

# Задача 4: Оптимизация типа данных "object"
for col in sample_data.select_dtypes(include=['object']).columns:
    if sample_data[col].nunique() / len(sample_data[col]) < 0.5:
        sample_data[col] = sample_data[col].astype('category')

# Задача 5: Понижающее преобразование типов "int"
int_cols = sample_data.select_dtypes(include=['int']).columns
for col in int_cols:
    sample_data[col] = pd.to_numeric(sample_data[col], downcast='integer')

# Задача 6: Понижающее преобразование типов "float"
float_cols = sample_data.select_dtypes(include=['float']).columns
for col in float_cols:
    sample_data[col] = pd.to_numeric(sample_data[col], downcast='float')

# Задача 7: Повторный анализ памяти
optimized_memory = sample_data.memory_usage(deep=True).sum() / (1024 ** 2)
print(f"Объем памяти после оптимизации: {optimized_memory:.2f} МБ")

# Сравнение памяти
memory_comparison = {
    "File_Size_MB": file_size,
    "Original_Memory_MB": data_memory,
    "Optimized_Memory_MB": optimized_memory
}
with open("memory_comparison.json", "w") as f:
    json.dump(memory_comparison, f, indent=4)

# Задача 8: Работа с поднабором данных и сохранение
selected_columns = sample_data.columns[:10]  # Произвольные 10 колонок
subset_file = "optimized_subset.csv"

dtype_mapping = {col: "str" for col in selected_columns if col in [7, 8]}  # Для смешанных типов

chunk_list = []
for chunk in pd.read_csv(file_path, chunksize=chunk_size, usecols=selected_columns, dtype=dtype_mapping, low_memory=False):
    # Преобразование типов в каждом чанке
    for col in chunk.select_dtypes(include=['object']).columns:
        if chunk[col].nunique() / len(chunk[col]) < 0.5:
            chunk[col] = chunk[col].astype('category')

    chunk_list.append(chunk)

optimized_subset = pd.concat(chunk_list)
optimized_subset.to_csv(subset_file, index=False)

# Задача 9: Построение графиков
# Удаление строковых данных для корреляции
numeric_subset = optimized_subset.select_dtypes(include=['number'])

optimized_subset[selected_columns[0]].value_counts().plot(kind='line')
plt.title("Линейный график")
plt.show()

optimized_subset[selected_columns[1]].value_counts().plot(kind='bar')
plt.title("Столбчатый график")
plt.show()

optimized_subset[selected_columns[2]].value_counts().plot(kind='pie')
plt.title("Круговая диаграмма")
plt.show()

correlation_matrix = numeric_subset.corr()
plt.matshow(correlation_matrix)
plt.title("Корреляционная матрица", pad=20)
plt.colorbar()
plt.show()
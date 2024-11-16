# Найти публичный API, который возвращает JSON с некоторыми данными.
# Необходимо получить данные в формате JSON, преобразовать в html представление в зависимости от содержания.

import requests
from jinja2 import Template

url = "https://randomuser.me/api/"
response = requests.get(url)
data = response.json()

user = data['results'][0]
name = f"{user['name']['first']} {user['name']['last']}"
age = user['dob']['age']
email = user['email']
location = f"{user['location']['city']}, {user['location']['state']}, {user['location']['country']}"
picture = user['picture']['large']

html_template = """
<html>
<head><title>Пользователь</title></head>
<body>
    <h1>Профиль пользователя</h1>
    <img src="{{ picture }}" alt="Фото пользователя" width="200"/>
    <h2>Имя: {{ name }}</h2>
    <p>Возраст: {{ age }} лет</p>
    <p>Email: {{ email }}</p>
    <p>Местоположение: {{ location }}</p>
</body>
</html>
"""

template = Template(html_template)
html_content = template.render(name=name, age=age, email=email, location=location, picture=picture)

# 5. Сохраняем результат в HTML файл
with open('result_5.html', 'w', encoding='utf-8') as result:
    result.write(html_content)

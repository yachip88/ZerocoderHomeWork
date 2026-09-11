import json
import requests

print("=== Задание 1: Получение данных ===")
url = "https://api.github.com/search/repositories"
params = {"q": "language:html"}
response = requests.get(url, params=params)
print(f"Status code: {response.status_code}")
payload = response.json()
print("total_count:", payload.get("total_count"))
items = payload.get("items", [])[:3]
for item in items:
    print({"full_name": item.get("full_name"), "html_url": item.get("html_url"), "language": item.get("language")})

print("\n=== Задание 2: Параметры запроса ===")
url = "https://jsonplaceholder.typicode.com/posts"
params = {"userId": 1}
response = requests.get(url, params=params)
if response.status_code == 200:
    posts = response.json()
    for post in posts:
        print(post)
else:
    print("Error", response.status_code)

print("\n=== Задание 3: Отправка данных ===")
url = "https://jsonplaceholder.typicode.com/posts"
data = {"title": "foo", "body": "bar", "userId": 1}
response = requests.post(url, json=data)
print(f"Status code: {response.status_code}")
print("ответ -", response.json())

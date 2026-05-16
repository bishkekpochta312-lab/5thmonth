#!/usr/bin/env python3
import requests
import json

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc4OTY0NTM1LCJpYXQiOjE3Nzg5NjI3MzUsImp0aSI6IjM1NjQwZGNjZTZhYTQ3NTJhYWVjZDIyN2M1YzJjZTAwIiwidXNlcl9pZCI6IjUifQ.tFqCOp6UumNEgCTfPjsFIevL2IlCWmbMqNA2Xs2xibk"
BASE_URL = "http://127.0.0.1:8000/api/v1"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def print_response(response, title):
    print(f"\n{'='*50}")
    print(title)
    print(f"Статус: {response.status_code}")
    if response.status_code in [200, 201]:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print(f"Ошибка: {response.text}")
    print('='*50)

def test_api():
    print("="*60)
    print("ТЕСТИРОВАНИЕ API")
    print("="*60)
    
    # 1. Профиль
    response = requests.get(f"{BASE_URL}/users/profile/", headers=headers)
    print_response(response, "1. ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ")
    
    # 2. Создание категории
    data = {"name": "Тестовая категория API"}
    response = requests.post(f"{BASE_URL}/categories/", json=data, headers=headers)
    print_response(response, "2. СОЗДАНИЕ КАТЕГОРИИ")
    
    # 3. Создание товара
    data = {
        "title": "Тестовый товар API",
        "description": "Это полное и качественное описание тестового товара для проверки API",
        "price": 299.99,
        "category": 1
    }
    response = requests.post(f"{BASE_URL}/products/", json=data, headers=headers)
    print_response(response, "3. СОЗДАНИЕ ТОВАРА")
    
    if response.status_code == 201:
        product_id = response.json().get('id')
        
        # 4. Создание отзыва
        data = {
            "text": "Отличный товар! API работает корректно, все функции доступны. Рекомендую!",
            "stars": 5,
            "product": product_id
        }
        response = requests.post(f"{BASE_URL}/reviews/", json=data, headers=headers)
        print_response(response, "4. СОЗДАНИЕ ОТЗЫВА")
    
    # 5. Список категорий
    response = requests.get(f"{BASE_URL}/categories/")
    print_response(response, "5. СПИСОК КАТЕГОРИЙ")
    
    # 6. Список товаров
    response = requests.get(f"{BASE_URL}/products/")
    print_response(response, "6. СПИСОК ТОВАРОВ")
    
    # 7. Товары с отзывами
    response = requests.get(f"{BASE_URL}/products/reviews/")
    if response.status_code == 200:
        print(f"\n{'='*50}")
        print("7. ТОВАРЫ С ОТЗЫВАМИ")
        products = response.json()
        print(f"Найдено товаров: {len(products)}")
        for product in products[:3]:
            print(f"\n  📦 {product.get('title')}")
            print(f"  Цена: {product.get('price')}$")
            print(f"  Рейтинг: {product.get('rating', 'Нет оценок')}⭐")
            print(f"  Отзывов: {len(product.get('reviews', []))}")
            for review in product.get('reviews', [])[:2]:
                print(f"    💬 {review.get('stars')}⭐: {review.get('text')[:60]}...")
        print('='*50)
    
    # 8. Статистика
    print(f"\n{'='*50}")
    print("8. СТАТИСТИКА")
    categories = requests.get(f"{BASE_URL}/categories/").json()
    products = requests.get(f"{BASE_URL}/products/").json()
    reviews = requests.get(f"{BASE_URL}/reviews/").json()
    print(f"  📁 Категорий: {len(categories)}")
    print(f"  📦 Товаров: {len(products)}")
    print(f"  💬 Отзывов: {len(reviews)}")
    print('='*50)

if __name__ == "__main__":
    test_api()
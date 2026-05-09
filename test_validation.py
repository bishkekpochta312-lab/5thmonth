import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api/v1'

def test_category_validation():
    print("\n" + "="*60)
    print("ТЕСТИРОВАНИЕ ВАЛИДАЦИИ КАТЕГОРИЙ")
    print("="*60)
    
    tests = [
        ("Пустое имя", {"name": ""}, "Название категории не может быть пустым"),
        ("Короткое имя", {"name": "A"}, "должно содержать минимум 2 символа"),
        ("Длинное имя", {"name": "A" * 101}, "не может превышать 100 символов"),
        ("Строчная буква", {"name": "тест"}, "начинаться с заглавной буквы"),
        ("Недопустимые символы", {"name": "Тест@123"}, "не может содержать символ"),
        ("Существующее имя", {"name": "Электроника"}, "уже существует"),
        ("Правильная категория", {"name": "Автомобили"}, "должна создаться"),
    ]
    
    for test_name, data, expected_message in tests:
        response = requests.post(f'{BASE_URL}/categories/', json=data)
        print(f"\nТест: {test_name}")
        print(f"Данные: {data}")
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 400:
            error = response.json()
            print(f"✓ Валидация сработала: {error}")
        elif response.status_code == 201:
            print(f"✓ Успешно создано: {response.json()}")
            # Удаляем созданную категорию
            category_id = response.json()['id']
            requests.delete(f'{BASE_URL}/categories/{category_id}/')
        else:
            print(f"✗ Неожиданный статус: {response.status_code}")

def test_product_validation():
    print("\n" + "="*60)
    print("ТЕСТИРОВАНИЕ ВАЛИДАЦИИ ТОВАРОВ")
    print("="*60)
    
    tests = [
        ("Пустое название", {"title": "", "description": "Полное описание товара", "price": 100, "category": 9}, "не может быть пустым"),
        ("Короткое название", {"title": "AB", "description": "Полное описание товара", "price": 100, "category": 9}, "минимум 3 символа"),
        ("Пустое описание", {"title": "Тестовый товар", "description": "", "price": 100, "category": 9}, "не может быть пустым"),
        ("Короткое описание", {"title": "Тестовый товар", "description": "Коротко", "price": 100, "category": 9}, "минимум 10 символов"),
        ("Отрицательная цена", {"title": "Тестовый товар", "description": "Полное описание товара", "price": -10, "category": 9}, "должна быть больше 0"),
        ("Ноль цена", {"title": "Тестовый товар", "description": "Полное описание товара", "price": 0, "category": 9}, "больше 0"),
        ("Слишком высокая цена", {"title": "Тестовый товар", "description": "Полное описание товара", "price": 2000000, "category": 9}, "превышать 1 000 000"),
        ("Неверная категория", {"title": "Тестовый товар", "description": "Полное описание товара", "price": 100, "category": 999}, "не существует"),
        ("Правильный товар", {"title": "Тестовый товар Уник", "description": "Полное описание качественного тестового товара", "price": 100.50, "category": 9}, "должен создаться"),
    ]
    
    for test_name, data, expected_message in tests:
        response = requests.post(f'{BASE_URL}/products/', json=data)
        print(f"\nТест: {test_name}")
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 400:
            print(f"✓ Валидация сработала")
            print(f"  Ошибка: {response.json()}")
        elif response.status_code == 201:
            print(f"✓ Успешно создано: {response.json()['title']}")
            product_id = response.json()['id']
            requests.delete(f'{BASE_URL}/products/{product_id}/')
        else:
            print(f"✗ Неожиданный статус: {response.status_code}")

def test_review_validation():
    print("\n" + "="*60)
    print("ТЕСТИРОВАНИЕ ВАЛИДАЦИИ ОТЗЫВОВ")
    print("="*60)
    
    tests = [
        ("Пустой текст", {"text": "", "stars": 5, "product": 1}, "не может быть пустым"),
        ("Короткий текст", {"text": "Ок", "stars": 5, "product": 1}, "минимум 5 символов"),
        ("Рейтинг меньше 1", {"text": "Отличный товар!", "stars": 0, "product": 1}, "меньше 1"),
        ("Рейтинг больше 5", {"text": "Отличный товар!", "stars": 6, "product": 1}, "больше 5"),
        ("Рейтинг не целое", {"text": "Отличный товар!", "stars": 4.5, "product": 1}, "целым числом"),
        ("Неверный товар", {"text": "Хороший товар!", "stars": 5, "product": 999}, "не существует"),
        ("Правильный отзыв", {"text": "Отличный товар, очень доволен покупкой!", "stars": 5, "product": 1}, "должен создаться"),
    ]
    
    for test_name, data, expected_message in tests:
        response = requests.post(f'{BASE_URL}/reviews/', json=data)
        print(f"\nТест: {test_name}")
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 400:
            print(f"✓ Валидация сработала")
            print(f"  Ошибка: {response.json()}")
        elif response.status_code == 201:
            print(f"✓ Успешно создано: {response.json()['text'][:50]}...")
            review_id = response.json()['id']
            requests.delete(f'{BASE_URL}/reviews/{review_id}/')
        else:
            print(f"✗ Неожиданный статус: {response.status_code}")

def test_update_validation():
    print("\n" + "="*60)
    print("ТЕСТИРОВАНИЕ ВАЛИДАЦИИ ПРИ ОБНОВЛЕНИИ")
    print("="*60)
    
    # Сначала создаем категорию для теста
    response = requests.post(f'{BASE_URL}/categories/', json={"name": "Временная категория"})
    if response.status_code == 201:
        category_id = response.json()['id']
        
        # Тестируем обновление с невалидными данными
        print("\nТест: Обновление категории с невалидным именем")
        update_data = {"name": "a"}  # Слишком короткое
        response = requests.put(f'{BASE_URL}/categories/{category_id}/', json=update_data)
        print(f"Статус: {response.status_code}")
        if response.status_code == 400:
            print(f"✓ Валидация сработала: {response.json()}")
        
        # Удаляем тестовую категорию
        requests.delete(f'{BASE_URL}/categories/{category_id}/')
    
    # Тест обновления товара
    print("\nТест: Обновление товара с невалидной ценой")
    update_data = {"price": -50}
    response = requests.patch(f'{BASE_URL}/products/1/', json=update_data)
    print(f"Статус: {response.status_code}")
    if response.status_code == 400:
        print(f"✓ Валидация сработала: {response.json()}")
    
    # Тест обновления отзыва
    print("\nТест: Обновление отзыва с невалидным рейтингом")
    update_data = {"stars": 10}
    response = requests.patch(f'{BASE_URL}/reviews/1/', json=update_data)
    print(f"Статус: {response.status_code}")
    if response.status_code == 400:
        print(f"✓ Валидация сработала: {response.json()}")

if __name__ == '__main__':
    print("🔍 НАЧАЛО ТЕСТИРОВАНИЯ ВАЛИДАЦИИ API")
    print("="*60)
    
    test_category_validation()
    test_product_validation()
    test_review_validation()
    test_update_validation()
    
    print("\n" + "="*60)
    print("✅ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("="*60)
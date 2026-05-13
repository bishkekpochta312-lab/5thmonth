#!/usr/bin/env python
import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_api.settings')
django.setup()

from product.models import Category, Product, Review
from users.models import User


def create_test_data():
    print("Начинаем создание тестовых данных...")
    
    # Создаем категории
    categories_data = [
        'Электроника',
        'Одежда', 
        'Книги',
        'Дом и сад',
        'Спорт'
    ]
    
    categories = {}
    for cat_name in categories_data:
        category, created = Category.objects.get_or_create(name=cat_name)
        categories[cat_name] = category
        if created:
            print(f"  ✓ Создана категория: {cat_name}")
        else:
            print(f"  • Категория уже существует: {cat_name}")
    
    # Создаем товары (исправлено форматирование цен)
    products_data = [
        {
            'title': 'Смартфон iPhone 15',
            'description': 'Новейший смартфон от Apple с потрясающей камерой и длительным временем работы',
            'price': 999.99,
            'category_name': 'Электроника'
        },
        {
            'title': 'Ноутбук MacBook Pro',
            'description': 'Мощный ноутбук для профессионалов с чипом M3',
            'price': 1999.99,
            'category_name': 'Электроника'
        },
        {
            'title': 'Футболка хлопковая',
            'description': 'Удобная хлопковая футболка для повседневной носки',
            'price': 29.99,
            'category_name': 'Одежда'
        },
        {
            'title': 'Джинсы классические',
            'description': 'Классические джинсы синего цвета, 100% хлопок',
            'price': 79.99,
            'category_name': 'Одежда'
        },
        {
            'title': 'Python для начинающих',
            'description': 'Книга по программированию на Python для новичков',
            'price': 49.99,
            'category_name': 'Книги'
        },
        {
            'title': 'Django 4 для профессионалов',
            'description': 'Продвинутая книга по Django для опытных разработчиков',
            'price': 89.99,
            'category_name': 'Книги'
        },
        {
            'title': 'Набор садовых инструментов',
            'description': 'Полный набор инструментов для сада и огорода',
            'price': 149.99,
            'category_name': 'Дом и сад'
        },
        {
            'title': 'Футбольный мяч',
            'description': 'Профессиональный футбольный мяч',
            'price': 39.99,
            'category_name': 'Спорт'
        }
    ]
    
    products = []
    for prod_data in products_data:
        category = categories[prod_data['category_name']]
        product, created = Product.objects.get_or_create(
            title=prod_data['title'],
            defaults={
                'description': prod_data['description'],
                'price': prod_data['price'],  # Теперь числа с 2 знаками
                'category': category
            }
        )
        products.append(product)
        if created:
            print(f"  ✓ Создан товар: {product.title}")
        else:
            print(f"  • Товар уже существует: {product.title}")
    
    # Создаем отзывы
    reviews_data = [
        {'product_title': 'Смартфон iPhone 15', 'text': 'Отличный телефон! Батарея держит долго, камера превосходная.', 'stars': 5},
        {'product_title': 'Смартфон iPhone 15', 'text': 'Хороший телефон, но дороговат.', 'stars': 4},
        {'product_title': 'Ноутбук MacBook Pro', 'text': 'Лучший выбор для разработки. Работает быстро.', 'stars': 5},
        {'product_title': 'Ноутбук MacBook Pro', 'text': 'Хороший ноутбук, но греется при нагрузках.', 'stars': 4},
        {'product_title': 'Футболка хлопковая', 'text': 'Качественная футболка, ткань приятная.', 'stars': 5},
        {'product_title': 'Джинсы классические', 'text': 'Отличные джинсы, сидят идеально!', 'stars': 5},
        {'product_title': 'Python для начинающих', 'text': 'Отличная книга для начинающих!', 'stars': 5},
        {'product_title': 'Django 4 для профессионалов', 'text': 'Отличная книга для разработчиков.', 'stars': 5},
        {'product_title': 'Набор садовых инструментов', 'text': 'Хороший набор, все инструменты качественные.', 'stars': 4},
        {'product_title': 'Футбольный мяч', 'text': 'Отличный мяч, качественная обшивка.', 'stars': 5},
    ]
    
    for review_data in reviews_data:
        try:
            product = Product.objects.get(title=review_data['product_title'])
            review, created = Review.objects.get_or_create(
                text=review_data['text'],
                product=product,
                defaults={'stars': review_data['stars']}
            )
            if created:
                print(f"  ✓ Создан отзыв для: {product.title}")
        except Product.DoesNotExist:
            print(f"  ✗ Товар не найден: {review_data['product_title']}")
    
    print("\n" + "="*50)
    print("Статистика:")
    print(f"  Категорий: {Category.objects.count()}")
    print(f"  Товаров: {Product.objects.count()}")
    print(f"  Отзывов: {Review.objects.count()}")
    print("="*50)
    print("Тестовые данные успешно созданы!")


if __name__ == '__main__':
    create_test_data()
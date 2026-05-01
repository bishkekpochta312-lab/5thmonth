#!/usr/bin/env python
import os
import django

# Указываем настройки проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_api.settings')
django.setup()

from product.models import Category, Product, Review

def create_test_data():
    """Создание тестовых данных"""
    
    # Проверяем, есть ли уже данные
    if Category.objects.exists():
        print("Данные уже существуют. Очищаем...")
        Review.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
    
    # Создаем категории
    print("Создаем категории...")
    electronics = Category.objects.create(name='Электроника')
    clothing = Category.objects.create(name='Одежда')
    books = Category.objects.create(name='Книги')
    
    # Создаем товары
    print("Создаем товары...")
    product1 = Product.objects.create(
        title='Смартфон iPhone 15',
        description='Новейший смартфон от Apple с потрясающей камерой и длительным временем работы',
        price=999.99,
        category=electronics
    )
    
    product2 = Product.objects.create(
        title='Ноутбук MacBook Pro',
        description='Мощный ноутбук для профессионалов с чипом M3',
        price=1999.99,
        category=electronics
    )
    
    product3 = Product.objects.create(
        title='Футболка хлопковая',
        description='Удобная хлопковая футболка для повседневной носки, различные размеры',
        price=29.99,
        category=clothing
    )
    
    product4 = Product.objects.create(
        title='Джинсы классические',
        description='Классические джинсы синего цвета, 100% хлопок',
        price=79.99,
        category=clothing
    )
    
    product5 = Product.objects.create(
        title='Python для начинающих',
        description='Книга по программированию на Python для новичков',
        price=49.99,
        category=books
    )
    
    # Создаем отзывы
    print("Создаем отзывы...")
    Review.objects.create(
        text='Отличный телефон! Батарея держит долго, камера превосходная. Рекомендую!',
        product=product1
    )
    
    Review.objects.create(
        text='Телефон хороший, но дороговат. Качество на высоте.',
        product=product1
    )
    
    Review.objects.create(
        text='MacBook Pro - лучший выбор для разработки. Работает быстро и без лагов.',
        product=product2
    )
    
    Review.objects.create(
        text='Хороший ноутбук, но греется при нагрузках. В остальном отлично.',
        product=product2
    )
    
    Review.objects.create(
        text='Футболка качественная, ткань приятная. Размер соответствует описанию.',
        product=product3
    )
    
    Review.objects.create(
        text='Книга очень полезная для начинающих! Много примеров и понятное объяснение.',
        product=product5
    )
    
    print("\n" + "="*50)
    print("Тестовые данные успешно созданы!")
    print("="*50)
    print(f"Создано категорий: {Category.objects.count()}")
    print(f"Создано товаров: {Product.objects.count()}")
    print(f"Создано отзывов: {Review.objects.count()}")
    print("="*50)
    
    # Выводим список созданных категорий
    print("\nКатегории:")
    for cat in Category.objects.all():
        print(f"  - {cat.name}")
    
    print("\nТовары:")
    for prod in Product.objects.all():
        print(f"  - {prod.title} ({prod.category.name}) - ${prod.price}")

if __name__ == '__main__':
    create_test_data()
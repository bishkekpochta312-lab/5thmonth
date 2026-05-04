#!/usr/bin/env python
import os
import django
import random
from django.db.models import Avg, Count  # Добавьте эту строку импорта

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_api.settings')
django.setup()

from product.models import Category, Product, Review

def create_test_data():
    """Создание тестовых данных с рейтингами"""
    
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
    home = Category.objects.create(name='Дом и сад')
    sports = Category.objects.create(name='Спорт')
    
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
    
    product6 = Product.objects.create(
        title='Django 4 для профессионалов',
        description='Продвинутая книга по Django для опытных разработчиков',
        price=79.99,
        category=books
    )
    
    product7 = Product.objects.create(
        title='Набор садовых инструментов',
        description='Полный набор инструментов для сада и огорода',
        price=149.99,
        category=home
    )
    
    product8 = Product.objects.create(
        title='Футбольный мяч',
        description='Профессиональный футбольный мяч',
        price=39.99,
        category=sports
    )
    
    # Создаем отзывы с разными оценками
    print("Создаем отзывы с рейтингами...")
    
    # Отзывы для iPhone
    Review.objects.create(
        text='Отличный телефон! Батарея держит долго, камера превосходная. Рекомендую!',
        stars=5,
        product=product1
    )
    Review.objects.create(
        text='Телефон хороший, но дороговат. Качество на высоте.',
        stars=4,
        product=product1
    )
    Review.objects.create(
        text='Неплохо, но ожидал большего за такую цену',
        stars=3,
        product=product1
    )
    
    # Отзывы для MacBook
    Review.objects.create(
        text='MacBook Pro - лучший выбор для разработки. Работает быстро и без лагов.',
        stars=5,
        product=product2
    )
    Review.objects.create(
        text='Хороший ноутбук, но греется при нагрузках. В остальном отлично.',
        stars=4,
        product=product2
    )
    
    # Отзывы для футболки
    Review.objects.create(
        text='Футболка качественная, ткань приятная. Размер соответствует описанию.',
        stars=5,
        product=product3
    )
    Review.objects.create(
        text='Хорошая футболка, но быстро теряет цвет',
        stars=3,
        product=product3
    )
    
    # Отзывы для джинсов
    Review.objects.create(
        text='Отличные джинсы, сидят идеально!',
        stars=5,
        product=product4
    )
    
    # Отзывы для Python книги
    Review.objects.create(
        text='Книга очень полезная для начинающих! Много примеров и понятное объяснение.',
        stars=5,
        product=product5
    )
    Review.objects.create(
        text='Хорошая книга, но некоторые темы слишком поверхностно',
        stars=4,
        product=product5
    )
    
    # Отзывы для Django книги
    Review.objects.create(
        text='Отличная книга для тех, кто уже знаком с Python!',
        stars=5,
        product=product6
    )
    Review.objects.create(
        text='Хорошая книга, но немного устаревшая информация',
        stars=4,
        product=product6
    )
    Review.objects.create(
        text='Средненько, ожидал больше примеров',
        stars=3,
        product=product6
    )
    
    # Отзывы для садового набора
    Review.objects.create(
        text='Хороший набор, все инструменты качественные',
        stars=4,
        product=product7
    )
    
    # Отзывы для футбольного мяча
    Review.objects.create(
        text='Отличный мяч, качественная обшивка',
        stars=5,
        product=product8
    )
    Review.objects.create(
        text='Хороший мяч для тренировок',
        stars=4,
        product=product8
    )
    
    print("\n" + "="*60)
    print("Тестовые данные успешно созданы!")
    print("="*60)
    print(f"Создано категорий: {Category.objects.count()}")
    print(f"Создано товаров: {Product.objects.count()}")
    print(f"Создано отзывов: {Review.objects.count()}")
    print("="*60)
    
    # Выводим информацию с рейтингами - ИСПРАВЛЕННАЯ ЧАСТЬ
    print("\nКатегории с количеством товаров:")
    for cat in Category.objects.annotate(products_count=Count('products')):
        print(f"  - {cat.name} (товаров: {cat.products_count})")
    
    print("\nТовары с рейтингами:")
    for prod in Product.objects.all():
        rating_avg = prod.reviews.aggregate(Avg('stars'))['stars__avg']
        rating = round(rating_avg, 1) if rating_avg else "Нет оценок"
        print(f"  - {prod.title} | Категория: {prod.category.name} | Цена: ${prod.price} | Рейтинг: {rating}⭐ | Отзывов: {prod.reviews.count()}")

if __name__ == '__main__':
    create_test_data()
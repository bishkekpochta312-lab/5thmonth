from django.db import models


class Category(models.Model):
    """Модель категории товаров"""
    name = models.CharField(max_length=200, verbose_name='Название категории')
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель товара"""
    title = models.CharField(max_length=200, verbose_name='Название товара')
    description = models.TextField(verbose_name='Описание товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products',
        verbose_name='Категория'
    )
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
    
    def __str__(self):
        return self.title


class Review(models.Model):
    """Модель отзыва о товаре"""
    text = models.TextField(verbose_name='Текст отзыва')
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='reviews',
        verbose_name='Товар'
    )
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
    
    def __str__(self):
        return f'Отзыв на товар: {self.product.title}'
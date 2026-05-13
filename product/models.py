from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Category(models.Model):
    """Модель категории товаров"""
    name = models.CharField(
        max_length=200, 
        unique=True,  # Добавляем уникальность
        verbose_name='Название категории'
    )
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def clean(self):
        """Модельная валидация"""
        from .validators import CategoryValidators
        self.name = CategoryValidators.validate_name(self.name)
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Вызываем валидацию перед сохранением
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель товара"""
    title = models.CharField(
        max_length=200, 
        unique=True,  # Добавляем уникальность
        verbose_name='Название товара'
    )
    description = models.TextField(verbose_name='Описание товара')
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Цена'
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products',
        verbose_name='Категория'
    )
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-id']
    
    def clean(self):
        """Модельная валидация"""
        from .validators import ProductValidators
        self.title = ProductValidators.validate_title(self.title)
        self.description = ProductValidators.validate_description(self.description)
        self.price = ProductValidators.validate_price(self.price)
    
    # def save(self, *args, **kwargs):
    #     self.full_clean()  # Вызываем валидацию перед сохранением
    #     super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class Review(models.Model):
    """Модель отзыва о товаре"""
    text = models.TextField(verbose_name='Текст отзыва')
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Рейтинг',
        help_text='Оценка от 1 до 5'
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='reviews',
        verbose_name='Товар'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
    
    def clean(self):
        """Модельная валидация"""
        from .validators import ReviewValidators
        self.text = ReviewValidators.validate_text(self.text)
        self.stars = ReviewValidators.validate_stars(self.stars)
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Вызываем валидацию перед сохранением
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'Отзыв на товар: {self.product.title} - {self.stars}⭐'
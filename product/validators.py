from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Category, Product, Review


class CategoryValidators:
    """Валидаторы для категорий"""
    
    @staticmethod
    def validate_name(value):
        """Валидация имени категории"""
        if not value or not value.strip():
            raise serializers.ValidationError("Название категории не может быть пустым")
        
        if len(value) < 2:
            raise serializers.ValidationError("Название категории должно содержать минимум 2 символа")
        
        if len(value) > 100:
            raise serializers.ValidationError("Название категории не может превышать 100 символов")
        
        if not value[0].isupper():
            raise serializers.ValidationError("Название категории должно начинаться с заглавной буквы")
        
        # Проверка на недопустимые символы
        invalid_chars = ['@', '#', '$', '%', '^', '&', '*', '(', ')', '=', '+', '[', ']', '{', '}']
        for char in invalid_chars:
            if char in value:
                raise serializers.ValidationError(f"Название категории не может содержать символ '{char}'")
        
        return value.strip()
    
    @staticmethod
    def validate_unique_name(value, exclude_id=None):
        """Проверка уникальности имени категории"""
        queryset = Category.objects.filter(name__iexact=value.strip())
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        
        if queryset.exists():
            raise serializers.ValidationError(f"Категория с названием '{value}' уже существует")
        
        return value


class ProductValidators:
    """Валидаторы для товаров"""
    
    @staticmethod
    def validate_title(value):
        """Валидация названия товара"""
        if not value or not value.strip():
            raise serializers.ValidationError("Название товара не может быть пустым")
        
        if len(value) < 3:
            raise serializers.ValidationError("Название товара должно содержать минимум 3 символа")
        
        if len(value) > 200:
            raise serializers.ValidationError("Название товара не может превышать 200 символов")
        
        # Проверка на дублирование названия
        if Product.objects.filter(title__iexact=value.strip()).exists():
            raise serializers.ValidationError(f"Товар с названием '{value}' уже существует")
        
        return value.strip()
    
    @staticmethod
    def validate_description(value):
        """Валидация описания товара"""
        if not value or not value.strip():
            raise serializers.ValidationError("Описание товара не может быть пустым")
        
        if len(value) < 10:
            raise serializers.ValidationError("Описание товара должно содержать минимум 10 символов")
        
        if len(value) > 5000:
            raise serializers.ValidationError("Описание товара не может превышать 5000 символов")
        
        # Проверка на слишком короткие слова
        words = value.split()
        if len(words) < 3:
            raise serializers.ValidationError("Описание должно содержать хотя бы 3 слова")
        
        return value.strip()
    
    @staticmethod
    def validate_price(value):
        """Валидация цены товара"""
        if value is None:
            raise serializers.ValidationError("Цена товара обязательна")
        
        if not isinstance(value, (int, float)):
            raise serializers.ValidationError("Цена должна быть числом")
        
        if value <= 0:
            raise serializers.ValidationError("Цена товара должна быть больше 0")
        
        if value > 1000000:
            raise serializers.ValidationError("Цена товара не может превышать 1 000 000")
        
        # Проверка на количество знаков после запятой
        if isinstance(value, float):
            decimal_str = str(value).split('.')[-1]
            if len(decimal_str) > 2:
                raise serializers.ValidationError("Цена может содержать не более 2 знаков после запятой")
        
        return round(value, 2)
    
    @staticmethod
    def validate_category(value):
        """Валидация категории товара"""
        if not value:
            raise serializers.ValidationError("Категория товара обязательна")
        
        if not isinstance(value, Category):
            if not Category.objects.filter(id=value).exists():
                raise serializers.ValidationError(f"Категория с id={value} не существует")
        
        return value


class ReviewValidators:
    """Валидаторы для отзывов"""
    
    @staticmethod
    def validate_text(value):
        """Валидация текста отзыва"""
        if not value or not value.strip():
            raise serializers.ValidationError("Текст отзыва не может быть пустым")
        
        if len(value) < 5:
            raise serializers.ValidationError("Текст отзыва должен содержать минимум 5 символов")
        
        if len(value) > 2000:
            raise serializers.ValidationError("Текст отзыва не может превышать 2000 символов")
        
        # Проверка на слишком короткое сообщение
        words = value.split()
        if len(words) < 2:
            raise serializers.ValidationError("Отзыв должен содержать хотя бы 2 слова")
        
        # Проверка на повторяющиеся символы
        import re
        if re.search(r'(.)\1{4,}', value):
            raise serializers.ValidationError("Текст отзыва не должен содержать более 4 повторяющихся символов подряд")
        
        return value.strip()
    
    @staticmethod
    def validate_stars(value):
        """Валидация рейтинга отзыва"""
        if value is None:
            raise serializers.ValidationError("Рейтинг обязателен")
        
        if not isinstance(value, int):
            try:
                value = int(value)
            except (ValueError, TypeError):
                raise serializers.ValidationError("Рейтинг должен быть целым числом")
        
        if value < 1:
            raise serializers.ValidationError("Рейтинг не может быть меньше 1")
        
        if value > 5:
            raise serializers.ValidationError("Рейтинг не может быть больше 5")
        
        # Проверка, что рейтинг целое число
        if not isinstance(value, int):
            raise serializers.ValidationError("Рейтинг должен быть целым числом (1, 2, 3, 4 или 5)")
        
        return value
    
    @staticmethod
    def validate_product(value):
        """Валидация товара для отзыва"""
        if not value:
            raise serializers.ValidationError("Товар для отзыва обязателен")
        
        if not isinstance(value, Product):
            if not Product.objects.filter(id=value).exists():
                raise serializers.ValidationError(f"Товар с id={value} не существует")
        
        return value
    
    @staticmethod
    def validate_unique_review(product_id, user_session=None):
        """Проверка на повторный отзыв (опционально)"""
        # Эта валидация может быть расширена для пользователей
        # Сейчас просто проверяем количество отзывов на товар
        reviews_count = Review.objects.filter(product_id=product_id).count()
        if reviews_count > 50:
            raise serializers.ValidationError(f"Товар уже имеет {reviews_count} отзывов. Новые отзывы временно ограничены")
        
        return True


class CommonValidators:
    """Общие валидаторы"""
    
    @staticmethod
    def validate_id(value):
        """Валидация ID"""
        if not isinstance(value, int):
            try:
                value = int(value)
            except (ValueError, TypeError):
                raise ValidationError("ID должен быть целым числом")
        
        if value <= 0:
            raise ValidationError("ID должен быть положительным числом")
        
        return value
    
    @staticmethod
    def sanitize_text(value):
        """Очистка текста от опасных символов"""
        if value:
            # Замена потенциально опасных HTML тегов
            import re
            value = re.sub(r'<[^>]+>', '', value)
            # Удаление лишних пробелов
            value = ' '.join(value.split())
        return value
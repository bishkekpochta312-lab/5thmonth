from rest_framework import serializers
from django.db.models import Avg
from .models import Category, Product, Review
from .validators import CategoryValidators, ProductValidators, ReviewValidators, CommonValidators


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категории с количеством товаров"""
    products_count = serializers.IntegerField(source='products.count', read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления категории с валидацией"""
    
    class Meta:
        model = Category
        fields = ['id', 'name']
    
    def validate_name(self, value):
        """Валидация имени категории"""
        # Базовая валидация
        value = CategoryValidators.validate_name(value)
        
        # Проверка уникальности
        instance = self.instance
        exclude_id = instance.id if instance else None
        value = CategoryValidators.validate_unique_name(value, exclude_id)
        
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзыва"""
    product_title = serializers.ReadOnlyField(source='product.title')
    
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'product', 'product_title']


class ReviewCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления отзыва с валидацией"""
    
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'product']
    
    def validate_text(self, value):
        """Валидация текста отзыва"""
        return ReviewValidators.validate_text(value)
    
    def validate_stars(self, value):
        """Валидация рейтинга"""
        return ReviewValidators.validate_stars(value)
    
    def validate_product(self, value):
        """Валидация товара"""
        return ReviewValidators.validate_product(value)
    
    def validate(self, data):
        """Дополнительная валидация при создании"""
        # Проверка на количество отзывов
        if not self.instance:  # Только при создании
            product = data.get('product')
            if product:
                ReviewValidators.validate_unique_review(product.id)
        
        # Очистка текста от опасных символов
        if 'text' in data:
            data['text'] = CommonValidators.sanitize_text(data['text'])
        
        return data


class ProductListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка товаров (без отзывов)"""
    category_name = serializers.ReadOnlyField(source='category.name')
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'category_name']


class ProductDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детального просмотра товара"""
    category_name = serializers.ReadOnlyField(source='category.name')
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'category_name', 'reviews', 'rating']
    
    def get_rating(self, obj):
        rating_avg = obj.reviews.aggregate(Avg('stars'))['stars__avg']
        if rating_avg is not None:
            return round(rating_avg, 1)
        return None


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления товара с валидацией"""
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category']
    
    def validate_title(self, value):
        """Валидация названия товара"""
        return ProductValidators.validate_title(value)
    
    def validate_description(self, value):
        """Валидация описания товара"""
        return ProductValidators.validate_description(value)
    
    def validate_price(self, value):
        """Валидация цены"""
        return ProductValidators.validate_price(value)
    
    def validate_category(self, value):
        """Валидация категории"""
        return ProductValidators.validate_category(value)
    
    def validate(self, data):
        """Общая валидация"""
        # Очистка текстовых полей
        if 'title' in data:
            data['title'] = CommonValidators.sanitize_text(data['title'])
        if 'description' in data:
            data['description'] = CommonValidators.sanitize_text(data['description'])
        
        return data


class ProductWithReviewsSerializer(serializers.ModelSerializer):
    """Сериализатор для товара с отзывами и средним рейтингом"""
    category_name = serializers.ReadOnlyField(source='category.name')
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'category_name', 'reviews', 'rating']
    
    def get_rating(self, obj):
        rating_avg = obj.reviews.aggregate(Avg('stars'))['stars__avg']
        if rating_avg is not None:
            return round(rating_avg, 1)
        return None
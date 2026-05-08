from rest_framework import serializers
from django.db.models import Avg
from .models import Category, Product, Review


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категории с количеством товаров"""
    products_count = serializers.IntegerField(source='products.count', read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления категории"""
    class Meta:
        model = Category
        fields = ['id', 'name']


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзыва"""
    product_title = serializers.ReadOnlyField(source='product.title')
    
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'product', 'product_title']


class ReviewCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления отзыва"""
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'product']


class ProductWithReviewsSerializer(serializers.ModelSerializer):
    """Сериализатор для товара с отзывами и средним рейтингом"""
    category_name = serializers.ReadOnlyField(source='category.name')
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'category_name', 'reviews', 'rating']
    
    def get_rating(self, obj):
        """Вычисляем средний рейтинг всех отзывов товара"""
        rating_avg = obj.reviews.aggregate(Avg('stars'))['stars__avg']
        if rating_avg is not None:
            return round(rating_avg, 1)
        return None


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
    """Сериализатор для создания и обновления товара"""
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category']
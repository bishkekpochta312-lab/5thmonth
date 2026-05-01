from rest_framework import serializers
from .models import Category, Product, Review


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категории"""
    class Meta:
        model = Category
        fields = ['id', 'name']


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзыва"""
    class Meta:
        model = Review
        fields = ['id', 'text', 'product']


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для товара"""
    category_name = serializers.ReadOnlyField(source='category.name')
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'category_name', 'reviews']
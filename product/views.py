from rest_framework import generics
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer


class CategoryListAPIView(generics.ListAPIView):
    """Вывод списка категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailAPIView(generics.RetrieveAPIView):
    """Вывод одной категории"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


class ProductListAPIView(generics.ListAPIView):
    """Вывод списка товаров"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    """Вывод одного товара"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


class ReviewListAPIView(generics.ListAPIView):
    """Вывод списка отзывов"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDetailAPIView(generics.RetrieveAPIView):
    """Вывод одного отзыва"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'
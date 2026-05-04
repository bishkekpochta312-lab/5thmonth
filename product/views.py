from rest_framework import generics
from django.db.models import Avg, Count
from .models import Category, Product, Review
from .serializers import (
    CategorySerializer, 
    ProductListSerializer, 
    ProductDetailSerializer,
    ProductWithReviewsSerializer,
    ReviewSerializer
)


class CategoryListAPIView(generics.ListAPIView):
    """Вывод списка категорий с количеством товаров"""
    queryset = Category.objects.annotate(
        products_count=Count('products')
    )
    serializer_class = CategorySerializer


class CategoryDetailAPIView(generics.RetrieveAPIView):
    """Вывод одной категории"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


class ProductListAPIView(generics.ListAPIView):
    """Вывод списка товаров (без отзывов)"""
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    """Вывод одного товара с отзывами и рейтингом"""
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'id'


class ProductWithReviewsListAPIView(generics.ListAPIView):
    """Вывод списка товаров с их отзывами и средним баллом"""
    queryset = Product.objects.all()
    serializer_class = ProductWithReviewsSerializer


class ReviewListAPIView(generics.ListAPIView):
    """Вывод списка отзывов"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDetailAPIView(generics.RetrieveAPIView):
    """Вывод одного отзыва"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'
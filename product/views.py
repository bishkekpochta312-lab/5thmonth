# product/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404
from .models import Category, Product, Review
from .serializers import (
    CategorySerializer,
    CategoryCreateUpdateSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    ProductCreateUpdateSerializer,
    ProductWithReviewsSerializer,
    ReviewSerializer,
    ReviewCreateUpdateSerializer
)


# ==================== КАТЕГОРИИ (CBV) ====================

class CategoryListCreateView(generics.ListCreateAPIView):
    """
    GET: Вывод списка категорий с количеством товаров
    POST: Создание новой категории
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Category.objects.annotate(products_count=Count('products'))
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CategoryCreateUpdateSerializer
        return CategorySerializer
    
    def perform_create(self, serializer):
        serializer.save()


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Вывод одной категории
    PUT/PATCH: Обновление категории
    DELETE: Удаление категории
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()
    lookup_field = 'id'
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CategorySerializer
        return CategoryCreateUpdateSerializer
    
    def perform_destroy(self, instance):
        """Проверка перед удалением"""
        if instance.products.exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError({
                'error': f'Нельзя удалить категорию "{instance.name}", так как в ней есть товары'
            })
        instance.delete()


# ==================== ТОВАРЫ (CBV) ====================

class ProductListCreateView(generics.ListCreateAPIView):
    """
    GET: Вывод списка товаров (без отзывов)
    POST: Создание нового товара
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateUpdateSerializer
        return ProductListSerializer
    
    def perform_create(self, serializer):
        serializer.save()


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Вывод одного товара с отзывами и рейтингом
    PUT/PATCH: Обновление товара
    DELETE: Удаление товара
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()
    lookup_field = 'id'
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductDetailSerializer
        return ProductCreateUpdateSerializer
    
    def perform_destroy(self, instance):
        """Удаление товара с информацией"""
        instance.delete()


class ProductWithReviewsView(generics.ListAPIView):
    """
    GET: Вывод списка товаров с их отзывами и средним баллом
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductWithReviewsSerializer


# ==================== ОТЗЫВЫ (CBV) ====================

class ReviewListCreateView(generics.ListCreateAPIView):
    """
    GET: Вывод списка отзывов
    POST: Создание нового отзыва
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Review.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewCreateUpdateSerializer
        return ReviewSerializer
    
    def perform_create(self, serializer):
        serializer.save()


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Вывод одного отзыва
    PUT/PATCH: Обновление отзыва
    DELETE: Удаление отзыва
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Review.objects.all()
    lookup_field = 'id'
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReviewSerializer
        return ReviewCreateUpdateSerializer
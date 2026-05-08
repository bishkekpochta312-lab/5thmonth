from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
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


# ==================== КАТЕГОРИИ ====================

class CategoryListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: Вывод списка категорий с количеством товаров
    POST: Создание новой категории
    """
    queryset = Category.objects.annotate(
        products_count=Count('products')
    )
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CategoryCreateUpdateSerializer
        return CategorySerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Вывод одной категории
    PUT/PATCH: Обновление категории
    DELETE: Удаление категории
    """
    queryset = Category.objects.all()
    lookup_field = 'id'
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CategorySerializer
        return CategoryCreateUpdateSerializer
    
    def delete(self, request, *args, **kwargs):
        """Переопределяем delete для проверки наличия товаров"""
        instance = self.get_object()
        if instance.products.exists():
            return Response(
                {'error': f'Нельзя удалить категорию "{instance.name}", так как в ней есть товары'},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_destroy(instance)
        return Response(
            {'message': f'Категория "{instance.name}" успешно удалена'},
            status=status.HTTP_200_OK
        )


# ==================== ТОВАРЫ ====================

class ProductListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: Вывод списка товаров (без отзывов)
    POST: Создание нового товара
    """
    queryset = Product.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateUpdateSerializer
        return ProductListSerializer


class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Вывод одного товара с отзывами и рейтингом
    PUT/PATCH: Обновление товара
    DELETE: Удаление товара
    """
    queryset = Product.objects.all()
    lookup_field = 'id'
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductDetailSerializer
        return ProductCreateUpdateSerializer
    
    def delete(self, request, *args, **kwargs):
        """Переопределяем delete для проверки наличия отзывов"""
        instance = self.get_object()
        product_title = instance.title
        reviews_count = instance.reviews.count()
        
        self.perform_destroy(instance)
        
        return Response(
            {
                'message': f'Товар "{product_title}" успешно удален',
                'deleted_reviews': f'Было удалено {reviews_count} отзывов'
            },
            status=status.HTTP_200_OK
        )


class ProductWithReviewsListAPIView(generics.ListAPIView):
    """Вывод списка товаров с их отзывами и средним баллом"""
    queryset = Product.objects.all()
    serializer_class = ProductWithReviewsSerializer


# ==================== ОТЗЫВЫ ====================

class ReviewListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: Вывод списка отзывов
    POST: Создание нового отзыва
    """
    queryset = Review.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewCreateUpdateSerializer
        return ReviewSerializer
    
    def create(self, request, *args, **kwargs):
        """Создание отзыва с проверкой существования товара"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Проверяем, существует ли товар
        product_id = request.data.get('product')
        if not Product.objects.filter(id=product_id).exists():
            return Response(
                {'error': f'Товар с id={product_id} не существует'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ReviewRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Вывод одного отзыва
    PUT/PATCH: Обновление отзыва
    DELETE: Удаление отзыва
    """
    queryset = Review.objects.all()
    lookup_field = 'id'
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReviewSerializer
        return ReviewCreateUpdateSerializer
    
    def delete(self, request, *args, **kwargs):
        """Удаление отзыва с информацией в ответе"""
        instance = self.get_object()
        review_text = instance.text[:50]
        product_title = instance.product.title
        
        self.perform_destroy(instance)
        
        return Response(
            {
                'message': f'Отзыв "{review_text}..." успешно удален',
                'product': product_title
            },
            status=status.HTTP_200_OK
        )
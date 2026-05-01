from django.urls import path
from . import views

urlpatterns = [
    # Категории
    path('categories/', views.CategoryListAPIView.as_view(), name='category-list'),
    path('categories/<int:id>/', views.CategoryDetailAPIView.as_view(), name='category-detail'),
    
    # Товары
    path('products/', views.ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:id>/', views.ProductDetailAPIView.as_view(), name='product-detail'),
    
    # Отзывы
    path('reviews/', views.ReviewListAPIView.as_view(), name='review-list'),
    path('reviews/<int:id>/', views.ReviewDetailAPIView.as_view(), name='review-detail'),
]
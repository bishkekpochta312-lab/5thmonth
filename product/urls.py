from django.urls import path
from . import views

urlpatterns = [
    # Категории
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:id>/', views.CategoryDetailView.as_view(), name='category-detail'),
    
    # Товары
    path('products/', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:id>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/reviews/', views.ProductWithReviewsView.as_view(), name='product-with-reviews'),
    
    # Отзывы
    path('reviews/', views.ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:id>/', views.ReviewDetailView.as_view(), name='review-detail'),
]
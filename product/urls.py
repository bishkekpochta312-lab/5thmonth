from django.urls import path
from . import views

urlpatterns = [
    # Категории - полный CRUD
    path('categories/', views.CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:id>/', views.CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-detail'),
    
    # Товары - полный CRUD
    path('products/', views.ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:id>/', views.ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-detail'),
    path('products/reviews/', views.ProductWithReviewsListAPIView.as_view(), name='product-with-reviews'),
    
    # Отзывы - полный CRUD
    path('reviews/', views.ReviewListCreateAPIView.as_view(), name='review-list-create'),
    path('reviews/<int:id>/', views.ReviewRetrieveUpdateDestroyAPIView.as_view(), name='review-detail'),
]
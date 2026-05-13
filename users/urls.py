from django.urls import path
from . import views

urlpatterns = [
    path('users/register/', views.RegisterAPIView.as_view(), name='register'),
    path('users/confirm/', views.ConfirmEmailAPIView.as_view(), name='confirm'),
    path('users/resend-code/', views.ResendConfirmationCodeAPIView.as_view(), name='resend-code'),
    path('users/login/', views.LoginAPIView.as_view(), name='login'),
    path('users/profile/', views.ProfileAPIView.as_view(), name='profile'),
    path('users/logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('users/refresh/', views.RefreshTokenAPIView.as_view(), name='refresh'),
]
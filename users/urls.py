from django.urls import path
from . import views

urlpatterns = [
    # Регистрация и подтверждение
    path('users/register/', views.RegisterView.as_view(), name='register'),
    path('users/confirm/', views.ConfirmEmailView.as_view(), name='confirm'),
    path('users/resend-code/', views.ResendConfirmationCodeView.as_view(), name='resend-code'),
    
    # Авторизация
    path('users/login/', views.LoginView.as_view(), name='login'),
    path('users/logout/', views.LogoutView.as_view(), name='logout'),
    path('users/refresh/', views.RefreshTokenView.as_view(), name='refresh'),
    
    # Профиль и управление
    path('users/profile/', views.ProfileView.as_view(), name='profile'),
    path('users/change-password/', views.ChangePasswordView.as_view(), name='change-password'),
]
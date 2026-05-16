# users/views.py
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import (
    CustomUserCreateSerializer,
    CustomUserSerializer,
    EmailConfirmationSerializer,
    LoginSerializer
)
from .models import EmailConfirmationCode, User
import random
import string


# ==================== РЕГИСТРАЦИЯ (CBV) ====================

class RegisterView(generics.CreateAPIView):
    """
    POST: Регистрация нового пользователя
    """
    permission_classes = [AllowAny]
    serializer_class = CustomUserCreateSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'status': 'success',
            'message': 'Регистрация успешна. Подтвердите email.',
            'user': CustomUserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


# ==================== ПОДТВЕРЖДЕНИЕ (CBV) ====================

class ConfirmEmailView(APIView):
    """
    POST: Подтверждение email пользователя через код
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = EmailConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        confirmation_code = serializer.validated_data['confirmation_code']
        
        user.is_active = True
        user.is_verified = True
        user.save()
        
        confirmation_code.is_used = True
        confirmation_code.save()
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'status': 'success',
            'message': 'Email подтвержден',
            'user': CustomUserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class ResendConfirmationCodeView(APIView):
    """
    POST: Повторная отправка кода подтверждения
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response({
                'error': 'Email обязателен'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                'error': 'Пользователь с таким email не найден'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if user.is_verified:
            return Response({
                'error': 'Пользователь уже подтвержден'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Удаляем старые коды
        EmailConfirmationCode.objects.filter(user=user).delete()
        
        # Генерируем новый код
        code = ''.join(random.choices(string.digits, k=6))
        EmailConfirmationCode.objects.create(user=user, code=code)
        
        print(f"\n{'='*50}")
        print(f"Новый код подтверждения для {user.email}: {code}")
        print(f"{'='*50}\n")
        
        return Response({
            'status': 'success',
            'message': 'Новый код отправлен на email'
        }, status=status.HTTP_200_OK)


# ==================== АВТОРИЗАЦИЯ (CBV) ====================

class LoginView(APIView):
    """
    POST: Авторизация пользователя и получение токенов
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            request,
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        
        if not user:
            return Response({
                'error': 'Неверные учетные данные'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_verified:
            return Response({
                'error': 'Пользователь не подтвержден. Подтвердите email.',
                'need_confirmation': True
            }, status=status.HTTP_403_FORBIDDEN)
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': CustomUserSerializer(user).data
        })


class LogoutView(APIView):
    """
    POST: Выход из системы (blacklist refresh token)
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                'status': 'success',
                'message': 'Выход выполнен успешно'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'Неверный токен'
            }, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):
    """
    POST: Обновление access токена
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return Response({
                'error': 'Refresh token обязателен'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh_token)
            return Response({
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        except Exception:
            return Response({
                'error': 'Неверный refresh token'
            }, status=status.HTTP_401_UNAUTHORIZED)


# ==================== ПРОФИЛЬ (CBV) ====================

class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET: Получение профиля пользователя
    PUT/PATCH: Обновление профиля пользователя
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer
    
    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    """
    POST: Смена пароля пользователя
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        new_password2 = request.data.get('new_password2')
        
        if not all([old_password, new_password, new_password2]):
            return Response({
                'error': 'Все поля обязательны'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if new_password != new_password2:
            return Response({
                'error': 'Новые пароли не совпадают'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        
        if not user.check_password(old_password):
            return Response({
                'error': 'Неверный текущий пароль'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        
        return Response({
            'status': 'success',
            'message': 'Пароль успешно изменен. Войдите снова с новым паролем.'
        }, status=status.HTTP_200_OK)
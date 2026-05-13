from rest_framework import status
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


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = CustomUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'status': 'success',
                'message': 'Регистрация успешна. Подтвердите email.',
                'user': CustomUserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmEmailAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = EmailConfirmationSerializer(data=request.data)
        if serializer.is_valid():
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendConfirmationCodeAPIView(APIView):
    """Повторная отправка кода подтверждения"""
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


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            
            if not user:
                return Response({'error': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)
            
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)


class LogoutAPIView(APIView):
    """Выход из системы"""
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
        except Exception:
            return Response({
                'status': 'error',
                'message': 'Неверный токен'
            }, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenAPIView(APIView):
    """Обновление access токена"""
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
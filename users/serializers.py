from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, EmailConfirmationCode  # Уберите UserProfile
import random
import string


class CustomUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'password', 'password2']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return value
    
    def create(self, validated_data):
        validated_data.pop('password2')
        
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        user.is_active = False
        user.is_verified = False
        user.save()
        
        code = ''.join(random.choices(string.digits, k=6))
        EmailConfirmationCode.objects.create(user=user, code=code)
        
        print(f"\n{'='*50}")
        print(f"Код подтверждения для {user.email}: {code}")
        print(f"{'='*50}\n")
        
        return user


class CustomUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'full_name', 'is_verified']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class EmailConfirmationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    
    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")
        
        try:
            confirmation_code = EmailConfirmationCode.objects.get(user=user, code=attrs['code'])
        except EmailConfirmationCode.DoesNotExist:
            raise serializers.ValidationError("Неверный код")
        
        if not confirmation_code.is_valid():
            raise serializers.ValidationError("Код истек")
        
        attrs['user'] = user
        attrs['confirmation_code'] = confirmation_code
        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
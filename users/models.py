# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
import random
import string


class User(AbstractUser):
    """Расширенная модель пользователя"""
    email = models.EmailField(unique=True, verbose_name='Email')
    is_active = models.BooleanField(default=False, verbose_name='Активен')
    is_verified = models.BooleanField(default=False, verbose_name='Подтвержден')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.email}"


class EmailConfirmationCode(models.Model):
    """Модель кода подтверждения email"""
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='confirmation_code',
        verbose_name='Пользователь'
    )
    code = models.CharField(max_length=6, unique=True, verbose_name='Код подтверждения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    expires_at = models.DateTimeField(verbose_name='Дата истечения')
    is_used = models.BooleanField(default=False, verbose_name='Использован')
    
    class Meta:
        verbose_name = 'Код подтверждения'
        verbose_name_plural = 'Коды подтверждения'
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            from django.conf import settings
            self.expires_at = timezone.now() + timedelta(
                minutes=getattr(settings, 'CONFIRMATION_CODE_EXPIRATION_MINUTES', 30)
            )
        super().save(*args, **kwargs)
    
    def is_valid(self):
        return not self.is_used and self.expires_at > timezone.now()
    
    def __str__(self):
        return f"Код для {self.user.email}: {self.code}"
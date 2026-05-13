# users/admin.py
from django.contrib import admin
from .models import User, EmailConfirmationCode

admin.site.register(User)
admin.site.register(EmailConfirmationCode)
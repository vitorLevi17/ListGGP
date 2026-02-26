from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Certifique-se de apagar aquela linha "from .models import ListGGP" se ela ainda estiver aí!

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
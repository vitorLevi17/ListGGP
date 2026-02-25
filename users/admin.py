from django.contrib.auth.models import User
from django.contrib import admin

# Certifique-se de apagar aquela linha "from .models import ListGGP" se ela ainda estiver aí!

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

# 1. Desregistra o User padrão do Django
admin.site.unregister(User)

# 2. Registra o User novamente, mas agora usando a sua configuração
admin.site.register(User, UserAdmin)
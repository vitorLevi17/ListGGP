from django.contrib import admin
from .models import Aula

class ListAula(admin.ModelAdmin):
    list_display = ("nm_aula", 
    "descricao",
    "palestrante",
    "carga_horaria")

admin.site.register(Aula,ListAula)
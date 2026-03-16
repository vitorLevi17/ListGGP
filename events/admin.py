from django.contrib import admin
from .models import Aula,Treinamento

class ListAula(admin.ModelAdmin):
    list_display = ("nm_aula", 
    "descricao",
    "palestrante",
    "carga_horaria")
class ListTreinamento(admin.ModelAdmin):
    list_display = ("nm_evento",
                    "data",
                    "local",
                    "status",
                    "horario_final"
                    )
    filter_horizontal = ('aulas',)

admin.site.register(Aula,ListAula)
admin.site.register(Treinamento,ListTreinamento)
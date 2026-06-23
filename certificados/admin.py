from django.contrib import admin
from .models import Certificado

class ListCertificados(admin.ModelAdmin):
    list_display = ('nm_certificado',
        'carga_horaria', 
        'palestrante' ,
        'empresa',
        'descricao', 
        'url')
admin.site.register(Certificado,ListCertificados)

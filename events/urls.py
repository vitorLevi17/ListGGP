from django.urls import path
from .views import listar_treinamentos_marcados,conferir_treinamento

urlpatterns = [
    path('listar-eventos-marcados/',listar_treinamentos_marcados,name='listar-eventos-marcados'),
    path('conferir-treinamento/<int:treinamento_id>/',conferir_treinamento,name='conferir-treinamento'),
]

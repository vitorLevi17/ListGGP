from django.urls import path
from .views import *

urlpatterns = [
    path('listar-eventos-marcados/',listar_treinamentos_marcados,name='listar-eventos-marcados'),
    path('conferir-treinamento/<int:treinamento_id>/',conferir_treinamento,name='conferir-treinamento'),
    path('iniciar-treinamento/<int:treinamento_id>/',iniciar_treinamento,name='iniciar-treinamento'),
    path('adicionar-participante/<int:treinamento_id>/<str:matricula_participante>/',adicionar_participante,name='adicionar-participante'),
    path('finalizar-treinamento/<int:treinamento_id>/',finalizar_treinamento,name='finalizar-treinamento'),
    path('exportar-lista-treinamento/<int:treinamento_id>/',gerar_relatorio,name='exportar-lista-treinamento'),
    path('criar-evento/',criar_evento,name='criar-evento'),
    path('criar-aula/', criar_aula, name='criar-aula'),
    path('treinamentos-finalizados/',treinamentos_finalizados,name='treinamentos-finalizados'),
    path('cancelar-treinamento/<int:treinamento_id>/',cancelar_treinamento,name='cancelar-treinamento'),
    path('alterar-data-finalizacao/<int:treinamento_id>/',alterar_data_finalizacao,name='alterar-data-finalizacao')
]
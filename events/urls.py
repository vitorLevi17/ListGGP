from django.urls import path,include
from .views import listar_treinamentos_marcados

urlpatterns = [
    path('listar-eventos-marcados/',listar_treinamentos_marcados,name='listar-eventos-marcados'),
    #path('cadastrar-evento/',nome-da-view(name='events-cadastrar-evento'))   

]

from django.urls import path
from .views import *

urlpatterns = [
    path('pagina-inicial/', pagina_inicial, name='pagina-inicial'),
    path('cadastrar-certificado/',cadastrar_certificado,name='cadastrar-certificado'),
    path('listar-certificados-usuario/',listar_certificados_usuario,name='listar-certificados-usuario')
    ]
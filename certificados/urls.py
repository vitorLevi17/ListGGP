from django.urls import path
from .views import *

urlpatterns = [
    path('pagina-inicial/', pagina_inicial, name='pagina-inicial')
    ]
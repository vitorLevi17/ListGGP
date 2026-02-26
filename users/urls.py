from django.urls import path
from users.views import login_view,index,usuario_altera_senha

urlpatterns = [
    path('login/', login_view, name='login'),
    path('index/',index,name='index'),
    path('alterar_senha',usuario_altera_senha,name='usuario_altera_senha')
    ]
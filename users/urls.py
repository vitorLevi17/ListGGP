from django.urls import path
from users.views import login_view,index

urlpatterns = [
    path('login/', login_view, name='login'),
    path('index/',index,name='index')
    ]
from django.urls import path

from .views import *

urlpatterns = [
    path('', visualizarVip,
         name='visualizar_vip')
]

from django.urls import path

from .views import *

urlpatterns = [
    path('', visualizarLlantas,
         name='visualizar_llantas')
]

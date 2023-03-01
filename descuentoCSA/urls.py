from django.urls import path

from .views import *

urlpatterns = [
    path('', visualizarCSA, name='visualizar_csa')
]

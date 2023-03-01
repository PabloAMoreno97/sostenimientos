from django.urls import path

from .views import *

urlpatterns = [
    path('', visualizarOtrosDescuentos,
         name='visualizar_otros_descuentos')
]

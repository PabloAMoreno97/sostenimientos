from django.urls import path

from .views import *

urlpatterns = [
    path('', visualizarRutinas, name='visualizar_rutinas'),
    path('mensaje/<str:no_encontrados>', visualizarRutinas,
         name='visualizar_rutinas_mensaje'),
    path('actualizar/', actualizarRutinasRedirect,
         name='actualizar_rutinas_redirect')
]

from django.urls import path

from .views import *

urlpatterns = [
    path('', visualizarSostenimientos,
         name='visualizar_sostenimientos'),
    path('mensaje/<str:msg>', visualizarSostenimientos,
         name='visualizar_sostenimientos_mensaje'),
    path('actualizar/', actualizarSostenimientosRedirect,
         name='actualizar_sostenimientos'),
    path('justificar/', justificarSostenimientos,
         name='justificar_sostenimientos'),
    path('factura/<str:factura>', visualizar_factura, name='visualizar_factura')
]

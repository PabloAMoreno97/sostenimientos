from django.urls import path

from .views import *

urlpatterns = [
    path('', inicio, name='inicio'),
    path('mensaje/<str:msg>/<str:no_encontrados>',
         inicio, name='inicio_mensaje'),
    path('actualizar-sostenimientos/', actualizar_sostenimientos,
         name='actualizar_sostenimientos_redirect'),
    path('actualizar-rutinas/', actualizar_rutinas, name='actualizar_rutinas'),
    path('actualizar-csa/', actualizar_csa, name='actualizar_csa'),
    path('actualizar-vip/', actualizar_vip, name='actualizar_vip'),
    path('actualizar-llantas/', actualizar_llantas, name='actualizar_llantas'),
    path('actualizar-otros-descuentos/', actualizar_otros_descuentos,
         name='actualizar_otros_descuentos'),
    path('actualizar/', actualizar_todo, name='actualizar_todo'),
    path('generar-informe/', generar_informe, name='generar_informe')
]

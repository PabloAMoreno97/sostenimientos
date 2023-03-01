from django.contrib import admin

from .models import Factura, Articulo, Sostenimiento, Identificador, Grupo

# Register your models here.
admin.site.register(Factura)
admin.site.register(Articulo)
admin.site.register(Sostenimiento)
admin.site.register(Identificador)
admin.site.register(Grupo)

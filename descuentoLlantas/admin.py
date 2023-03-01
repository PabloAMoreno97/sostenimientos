from django.contrib import admin

from descuentoLlantas import models

# Register your models here.
admin.site.register(models.Marca)
admin.site.register(models.Llanta)
admin.site.register(models.Descuento)

from django.contrib import admin

from descuentoCSA import models

# Register your models here.
admin.site.register(models.Csa)
admin.site.register(models.TipoArticulo)
admin.site.register(models.Descuento)
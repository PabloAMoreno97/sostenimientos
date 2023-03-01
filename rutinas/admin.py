from django.contrib import admin

from rutinas import models

# Register your models here.

admin.site.register(models.Articulo)
admin.site.register(models.Rutina)
admin.site.register(models.TipoArticulo)
admin.site.register(models.Vehiculo)
admin.site.register(models.FiltroSustituto)

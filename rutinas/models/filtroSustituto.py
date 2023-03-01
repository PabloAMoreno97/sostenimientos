from django.db import models

from rutinas.models.tipoArticulo import TipoArticulo


class FiltroSustitutoManager(models.Manager):
    def crear_filtroSustituto(self, filtro):
        filtro_sustituto = self.create(
            ean=filtro.ean, nombre=filtro.nombre, tipo=filtro.tipo)
        return filtro_sustituto


class FiltroSustituto(models.Model):
    id = models.BigAutoField(primary_key=True)
    ean = models.CharField(max_length=20)
    nombre = models.CharField(max_length=255)
    tipo = models.ForeignKey(TipoArticulo, on_delete=models.DO_NOTHING,
                             related_name="filtrosSustitutos_tipoArticulo")

    objects = FiltroSustitutoManager()

    def __str__(self):
        return self.ean

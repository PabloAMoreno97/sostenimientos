from django.db import models

from .tipoArticulo import TipoArticulo


class ArticuloManager(models.Manager):
    def crear_articulo(self, articulo):
        nuevo_articulo = self.create(
            ean=articulo.ean, nombre=articulo.nombre, tipo=articulo.tipo)
        return nuevo_articulo


class Articulo(models.Model):
    id = models.BigAutoField(primary_key=True)
    ean = models.CharField(max_length=40)
    nombre = models.CharField(max_length=255)
    tipo = models.ForeignKey(
        TipoArticulo, related_name="articulo_tipoArticulo", on_delete=models.DO_NOTHING)

    objects = ArticuloManager()

    def __str__(self):
        return f'{self.tipo} {self.ean}'

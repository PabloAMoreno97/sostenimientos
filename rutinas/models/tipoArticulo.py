from django.db import models


class TipoArticuloManager(models.Manager):
    def crear_tipo_articulo(self, tipo):
        nuevo_tipo = self.create(nombre=tipo)
        return nuevo_tipo


class TipoArticulo(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    objects = TipoArticuloManager()

    def __str__(self):
        return self.nombre

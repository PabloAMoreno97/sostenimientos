from django.db import models

from .llanta import Llanta


class DescuentoManager(models.Manager):
    def crear_descuento(self, descuento):
        nuevoDescuento = self.create(
            llanta=descuento.llanta, porcentaje=descuento.porcentaje)
        return nuevoDescuento


class Descuento(models.Model):
    id = models.BigAutoField(primary_key=True)
    llanta = models.ForeignKey(
        Llanta, related_name="descuentoLlantas_llanta", on_delete=models.DO_NOTHING)
    porcentaje = models.IntegerField()

    objects = DescuentoManager()

    def __str__(self):
        return f'{self.llanta} {self.porcentaje}%'

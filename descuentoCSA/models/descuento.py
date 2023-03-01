from django.db import models

from .tipoArticulo import TipoArticulo
from .csa import Csa


class DescuentoManager(models.Manager):
    def crear_descuento(self, descuento):
        nuevo_descuento = self.create(csa=descuento.csa, descuento=descuento.descuento,
                                      tipoArticulo=descuento.tipoArticulo, origen=descuento.origen)
        return nuevo_descuento


class Descuento(models.Model):

    ORIGEN = (
        ("Repme", "Repme"),
        ("Ventanilla", "Ventanilla")
    )

    id = models.BigAutoField(primary_key=True)
    csa = models.ForeignKey(
        Csa, on_delete=models.DO_NOTHING, related_name="descuento_csa")
    descuento = models.IntegerField()
    tipoArticulo = models.ForeignKey(
        TipoArticulo, on_delete=models.DO_NOTHING, related_name="descuento_tipo")
    origen = models.CharField(choices=ORIGEN, max_length=15, default=1)

    objects = DescuentoManager()

    def __str__(self):
        return f'{self.csa.nombre} - {self.tipoArticulo} - {self.descuento}'

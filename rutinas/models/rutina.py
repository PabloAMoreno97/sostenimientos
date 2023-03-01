from django.db import models

from .vehiculo import Vehiculo
from .articulo import Articulo


class RutinaManager(models.Manager):
    def crear_rutina(self, rutina):
        rutinaNueva = self.create(vehiculo=rutina.vehiculo, articulo=rutina.articulo,
                                  precioUnitario=rutina.precioUnitario, cantidad=rutina.cantidad)
        return rutinaNueva


class Rutina(models.Model):
    id = models.BigAutoField(primary_key=True)
    vehiculo = models.ForeignKey(
        Vehiculo, on_delete=models.DO_NOTHING, related_name="rutina_vehiculo")
    articulo = models.ForeignKey(
        Articulo, on_delete=models.DO_NOTHING, related_name="rutina_Articulo")
    precioUnitario = models.IntegerField("Precio Unitario")
    cantidad = models.IntegerField()

    objects = RutinaManager()

    def __str__(self):
        return f'{self.vehiculo} {self.articulo.tipo}'

    def precioTotal(self):
        return self.precioUnitario*self.cantidad

    def formatear_precio(self, precio):
        precio_formateado = []
        for i, numero in enumerate(str(precio)[::-1]):
            if i == 3:
                precio_formateado.insert(0, ".")
                precio_formateado.insert(0, numero)
            elif i == 6:
                precio_formateado.insert(0, "'")
                precio_formateado.insert(0, numero)
            else:
                precio_formateado.insert(0, numero)
        precio_formateado = "".join(precio_formateado)
        return precio_formateado

    def precio_unitario_formateado(self):
        return self.formatear_precio(self.precioUnitario)

    def precio_total_formateado(self):
        precioTotal = self.precioUnitario * self.cantidad
        return self.formatear_precio(precioTotal)

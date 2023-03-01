from django.db import models


class ManagerDescuentoBateria(models.Manager):
    def crear_descuento_bateria(self, descuentoBateria):
        nuevo_descuento_bateria = self.create(
            precioUnitario=descuentoBateria.precioUnitario, ean=descuentoBateria.ean, nombre=descuentoBateria.nombre)
        return nuevo_descuento_bateria


class DescuentoBateria(models.Model):
    precioUnitario = models.IntegerField("Precio Unitario")
    ean = models.CharField(max_length=40, primary_key=True)
    nombre = models.CharField(max_length=200)

    objects = ManagerDescuentoBateria()

    def __str__(self):
        return f'{self.ean} {self.nombre} {self.precioUnitario}'

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

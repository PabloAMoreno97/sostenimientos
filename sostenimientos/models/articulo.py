from django.db import models
from .factura import Factura


class ArticuloManager(models.Manager):
    def crear_articulo(self, articulo):
        articuloNuevo = self.create(ean=articulo.ean, nombre=articulo.nombre, cantidad=articulo.cantidad, precioInicial=articulo.precioInicial, precioFinal=articulo.precioFinal, descuento=articulo.descuento,
                                    precioDescuento=articulo.precioDescuento, sostenimientoPrecio=articulo.sostenimientoPrecio, promocionAplicada=articulo.promocionAplicada, linea=articulo.linea, factura=articulo.factura,)
        return articuloNuevo


class Articulo(models.Model):
    id = models.BigAutoField(primary_key=True)
    ean = models.CharField(max_length=30)
    nombre = models.CharField(max_length=255)
    cantidad = models.IntegerField()
    precioInicial = models.IntegerField()
    precioFinal = models.IntegerField()
    descuento = models.IntegerField()
    precioDescuento = models.IntegerField()
    sostenimientoPrecio = models.CharField(max_length=50)
    promocionAplicada = models.CharField(max_length=50)
    linea = models.CharField(max_length=10)
    factura = models.ForeignKey(
        Factura, on_delete=models.DO_NOTHING, related_name="articulo_factura")

    objects = ArticuloManager()

    def __str__(self):
        return f"{self.ean} {self.nombre} - {self.factura.numero}"

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

    def precio_inicial_formateado(self):
        inicial = self.formatear_precio(self.precioInicial)
        return inicial

    def precio_final_formateado(self):
        final = self.formatear_precio(self.precioFinal)
        return final

    def precio_descuento_formateado(self):
        descuento = self.formatear_precio(self.precioDescuento)
        return descuento

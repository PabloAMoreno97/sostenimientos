from django.db import models


class FacturaManager(models.Manager):
    def crear_factura(self, factura):
        facturaNueva = self.create(numero=factura.numero, fecha=factura.fecha, cajero=factura.cajero, cliente=factura.cliente, tipoDocumento=factura.tipoDocumento,
                                   nombreCliente=factura.nombreCliente, observacion=factura.observacion, unidadNegocio=factura.unidadNegocio)
        return facturaNueva


class Factura(models.Model):
    numero = models.CharField(max_length=50, primary_key=True)
    fecha = models.DateTimeField()
    cajero = models.CharField(max_length=50)
    cliente = models.CharField(max_length=50)
    tipoDocumento = models.CharField(max_length=10)
    nombreCliente = models.CharField(max_length=50)
    observacion = models.CharField(max_length=500)
    unidadNegocio = models.CharField(max_length=15)

    objects = FacturaManager()

    def __str__(self):
        return f'{self.numero} - {self.cliente} - {self.observacion}'

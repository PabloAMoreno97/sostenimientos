from django.db import models

from .articulo import Articulo
from .identificador import Identificador
from .grupo import Grupo


class SostenimientoManager(models.Manager):
    def crear_sostenimiento(self, sostenimiento):
        sostenimientoNuevo = self.create(
            articulo=sostenimiento.articulo, justificacion=sostenimiento.justificacion, identificador=sostenimiento.identificador, grupo=sostenimiento.grupo)
        return sostenimientoNuevo


class Sostenimiento(models.Model):
    articulo = models.ForeignKey(
        Articulo, on_delete=models.DO_NOTHING, related_name="sostenimiento_articulo")
    justificacion = models.CharField(max_length=50)
    identificador = models.ForeignKey(
        Identificador, on_delete=models.DO_NOTHING, related_name="sostenimiento_identificador")
    grupo = models.ForeignKey(
        Grupo, on_delete=models.DO_NOTHING, related_name="sostenimiento_grupo", default=1
    )

    objects = SostenimientoManager()

    def __str__(self):
        return f'{self.articulo.factura.numero} - {self.articulo.ean} - {self.justificacion}'


'''

class Sostenimiento1:
    factura = str #factura
    fecha = str #factura
    tipoDoc = str #factura
    cliente = str #factura
    nombreCliente = str #factura
    ean = str #articulo
    articulo = str #articulo
    observaciones = str #factura
    coordinador = str #factura
    cantidad = str #articulo
    precioInicialUnitario = str #articulo
    precioFinal = str #articulo
    descto = str #articulo
    precioDescto = str #articulo
    sostenimientoPrecio = str #articulo
    un = str #factura
    promocionesAplicadas = str #articulo
    linea = str
    justificacion = str

    def __init__(self, factura, fecha, tipoDoc, cliente, nombreCliente, ean, articulo, observaciones, coordinador, cantidad, precioInicialUnitario, precioFinal, descto, precioDescto, sostenimientoPrecio, un, promocionesAplicadas):
        self.factura = factura
        self.fecha = fecha
        self.tipoDoc = tipoDoc
        self.cliente = cliente
        self.nobmreCliente = nombreCliente
        self.ean = ean
        self.articulo = articulo
        self.observaciones = observaciones
        self.coordinador = coordinador
        self.cantidad = cantidad
        self.precioInicialUnitario = precioInicialUnitario
        self.precioFinal = precioFinal
        self.descto = descto
        self.precioDescto = precioDescto
        self.sostenimientoPrecio = sostenimientoPrecio
        self.un = un
        self.promocionesAplicadas = promocionesAplicadas
        if "unlan" in self.observaciones or "UNLAN" in self.observaciones:
            self.linea = "BJ2037"
        elif "BJ" in self.observaciones:
            posicionLinea = self.observaciones.find("BJ")
            self.linea = self.observaciones[posicionLinea:posicionLinea+6]
        else:
            self.linea = None

        self.justificacion = None

    def sostenimientoRutina(self):
        if self.linea != None:
            print(self.linea)

    def mostrarJustificacion(self):
        if self.justificacion == None:
            print(self.factura, self.ean, "Sin justificar")
        else:
            print(self.factura, self.ean, self.justificacion)

'''

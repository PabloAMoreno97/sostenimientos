from django.db import models


class VehiculoManager(models.Manager):
    def crear_vehiculo(self, linea):
        vehiculo = self.create(linea=linea)
        return vehiculo


class Vehiculo(models.Model):
    id = models.BigAutoField(primary_key=True)
    linea = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.linea

    objects = VehiculoManager()

from django.db import models


class IdentificadorManager(models.Manager):
    def crear_identificador(self, identificador):
        nuevo_identificador = self.create(
            id=identificador.id, nombre=identificador.nombre)
        return nuevo_identificador


class Identificador(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)

    objects = IdentificadorManager()

    def __str__(self):
        return f'{self.id} - {self.nombre}'

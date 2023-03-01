from django.db import models


class MarcaManager(models.Manager):
    def crear_marca(self, marca):
        nueva_marca = self.create(nombre=marca)
        return nueva_marca


class Marca(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    objects = MarcaManager()

    def __str__(self):
        return self.nombre

from django.db import models

from .marca import Marca


class LlantaManager(models.Manager):
    def crear_llanta(self, llanta):
        nuevaLlanta = self.create(ean=llanta.ean, marca=llanta.marca)
        return nuevaLlanta


class Llanta(models.Model):
    ean = models.CharField(primary_key=True, max_length=50)
    marca = models.ForeignKey(
        Marca, related_name="llanta_marcaLlanta", on_delete=models.DO_NOTHING)
    objects = LlantaManager()

    def __str__(self):
        return f'{self.ean} {self.marca}'

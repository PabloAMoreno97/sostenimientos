from django.db import models


class CsaManager(models.Manager):
    def crear_csa(self, csa):
        nuevo_csa = self.create(documento=csa.documento, nombre=csa.nombre)
        return nuevo_csa


class Csa(models.Model):
    documento = models.CharField(max_length=40, primary_key=True)
    nombre = models.CharField(max_length=100)

    objects = CsaManager()

    def __str__(self):
        return f'{self.nombre}'

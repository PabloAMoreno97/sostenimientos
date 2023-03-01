from django.db import models

from .categoria import Categoria


class VipManager(models.Manager):
    def crear_vip(self, vip):
        nuevo_vip = self.create(documento=vip.documento,
                                nombre=vip.nombre, categoriaVip=vip.categoriaVip)
        return nuevo_vip


class Vip(models.Model):
    documento = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=200)
    categoriaVip = models.ForeignKey(
        Categoria, on_delete=models.DO_NOTHING, related_name="vip_categoriaVip")

    objects = VipManager()

    def __str__(self):
        return self.nombre

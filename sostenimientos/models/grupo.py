from django.db import models


class GrupoManager(models.Manager):
    def crear_grupo(self, grupo):
        grupo_nuevo = self.create(nombre=grupo)
        return grupo_nuevo


class Grupo(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=20)

    objects = GrupoManager()

    def __str__(self):
        return self.nombre

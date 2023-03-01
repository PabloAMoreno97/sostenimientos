from django.db import models


class CategoriaManager(models.Manager):
    def crear_categoria(self, categoria):
        nueva_categoria = self.create(nombre=categoria.nombre, aceite=categoria.aceite,
                                      colision=categoria.colision, cabina=categoria.cabina, cummins=categoria.cummins, filtro=categoria.filtro, llanta=categoria.llanta, motor=categoria.motor, repuestoGeneral=categoria.repuestoGeneral, rutina=categoria.rutina)
        return nueva_categoria


class Categoria(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    aceite = models.IntegerField()
    colision = models.IntegerField()
    cabina = models.IntegerField()
    cummins = models.IntegerField()
    filtro = models.IntegerField()
    llanta = models.IntegerField()
    motor = models.IntegerField()
    repuestoGeneral = models.IntegerField()
    rutina = models.IntegerField()

    objects = CategoriaManager()

    def __str__(self):
        return self.nombre

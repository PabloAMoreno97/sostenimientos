# Generated by Django 4.1.6 on 2023-02-24 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('descuentoVIP', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categoria',
            old_name='descuentoAceite',
            new_name='aceite',
        ),
        migrations.RenameField(
            model_name='categoria',
            old_name='descuentoCabina',
            new_name='cabina',
        ),
        migrations.RenameField(
            model_name='categoria',
            old_name='descuentoColision',
            new_name='colision',
        ),
        migrations.RenameField(
            model_name='categoria',
            old_name='descuentoCummins',
            new_name='cummins',
        ),
        migrations.RenameField(
            model_name='categoria',
            old_name='descuentoFiltro',
            new_name='filtro',
        ),
        migrations.RenameField(
            model_name='categoria',
            old_name='descuentoLlanta',
            new_name='llanta',
        ),
        migrations.RenameField(
            model_name='categoria',
            old_name='descuentoMotor',
            new_name='motor',
        ),
        migrations.RenameField(
            model_name='categoria',
            old_name='descuentoRepuestoGeneral',
            new_name='repuestoGeneral',
        ),
        migrations.RenameField(
            model_name='categoria',
            old_name='descuentoRutina',
            new_name='rutina',
        ),
    ]

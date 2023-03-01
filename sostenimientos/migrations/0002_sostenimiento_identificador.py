# Generated by Django 4.1.6 on 2023-02-24 04:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sostenimientos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sostenimiento',
            name='identificador',
            field=models.ForeignKey(default=233, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sostenimiento_identificador', to='sostenimientos.identificador'),
            preserve_default=False,
        ),
    ]

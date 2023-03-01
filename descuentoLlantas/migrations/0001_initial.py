# Generated by Django 4.1.6 on 2023-02-24 04:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Llanta',
            fields=[
                ('ean', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='llanta_marcaLlanta', to='descuentoLlantas.marca')),
            ],
        ),
        migrations.CreateModel(
            name='Descuento',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('porcentaje', models.IntegerField()),
                ('llanta', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='descuentoLlantas_llanta', to='descuentoLlantas.llanta')),
            ],
        ),
    ]
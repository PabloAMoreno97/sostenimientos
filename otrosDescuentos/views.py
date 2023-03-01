from django.shortcuts import render
import pandas as pd
from .models import DescuentoBateria
# Create your views here.


def listarDescuentosBateria():
    return DescuentoBateria.objects.all()


def visualizarOtrosDescuentos(request):
    actualizarOtrosDescuentos()
    lista_descuentosBateria = listarDescuentosBateria()
    return render(request, 'otrosDescuentos/index.html', {'baterias': lista_descuentosBateria})


def actualizarOtrosDescuentos():
    DescuentoBateria.objects.all().delete()
    lista_descuentosBateria = listarDescuentosBateria()
    efDescuentos = pd.ExcelFile("archivos_excel/descuentos.xlsx")
    dfBaterias = efDescuentos.parse("Baterias")
    for i in range(0, dfBaterias.iloc[:, 0].count()):
        ean = dfBaterias.iloc[i, 0]
        descripcion = dfBaterias.iloc[i, 1]
        precio = dfBaterias.iloc[i, 2]
        if lista_descuentosBateria.filter(ean=ean).exists():
            continue
        else:
            descuentoBateria = DescuentoBateria(
                ean=ean, nombre=descripcion, precioUnitario=precio)
            descuentoBateria = DescuentoBateria.objects.crear_descuento_bateria(
                descuentoBateria)

from django.shortcuts import render

import pandas as pd

from .models import Llanta, Marca, Descuento
from .forms import LlantasForm

# Create your views here.


def listarDescuentos():
    return Descuento.objects.all()


def visualizarLlantas(request):
    lista_descuentos = listarDescuentos()
    form = LlantasForm()
    if request.method == "POST":
        form = LlantasForm(request.POST)
        if form.is_valid():
            marca = form.cleaned_data.get('marca')
            if marca != None:
                lista_descuentos = lista_descuentos.filter(
                    llanta__marca__nombre=marca)
    return render(request, 'descuentoLlantas/index.html', {"descuentos": lista_descuentos, "form": form})


def actualizarLlantas():
    efDescuentos = pd.ExcelFile("archivos_excel/descuentos.xlsx")
    efLlantas = efDescuentos.parse("Llantas")
    lista_llantas = Llanta.objects.all()
    lista_marcas = Marca.objects.all()
    Descuento.objects.all().delete()
    lista_descuentos = Descuento.objects.all()
    for i in range(0, efLlantas.iloc[:, 0].count()):
        ean = efLlantas.iloc[i, 0]
        descuento = efLlantas.iloc[i, 2]*100
        marca = efLlantas.iloc[i, 3]
        if lista_marcas.filter(nombre=marca).exists():
            marca = lista_marcas.get(nombre=marca)
        else:
            marca = Marca.objects.crear_marca(marca)
        if lista_llantas.filter(ean=ean).exists():
            llanta = lista_llantas.get(ean=ean)
        else:
            llanta = Llanta(ean=ean, marca=marca)
            llanta = Llanta.objects.crear_llanta(llanta)
        if lista_descuentos.filter(llanta__ean=ean).exists():
            continue
        else:
            descuento = Descuento(llanta=llanta, porcentaje=descuento)
            descuento = Descuento.objects.crear_descuento(descuento)

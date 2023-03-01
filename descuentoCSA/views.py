from django.shortcuts import render

import pandas as pd

from .models import Csa, Descuento, TipoArticulo

from .forms import CsaForm
# Create your views here.


def visualizarCSA(request):
    form = CsaForm()
    lista_descuentos = Descuento.objects.all()
    if request.method == 'POST':
        form = CsaForm(request.POST)
        if form.is_valid():
            origen = form.cleaned_data.get('origen')
            csa = form.cleaned_data.get('csa')
            documento = form.cleaned_data.get('documento')
            if origen != 'Todos':
                lista_descuentos = lista_descuentos.filter(origen=origen)
            if csa != None:
                lista_descuentos = lista_descuentos.filter(csa__nombre=csa)
            if documento != None:
                lista_descuentos = lista_descuentos.filter(
                    csa__documento__icontains=documento)
    return render(request, 'descuentoCSA/index.html', {'descuentos': lista_descuentos, 'form': form})


def guardarDescuentoCSA(csa, descuento, tipoArticulo, origen):
    descuentoNuevo = Descuento(
        csa=csa, descuento=descuento, tipoArticulo=tipoArticulo, origen=origen)
    descuentoNuevo = Descuento.objects.crear_descuento(descuentoNuevo)
    return descuentoNuevo


def actualizarCSA():
    Descuento.objects.all().delete()
    Csa.objects.all().delete()
    efDescuentos = pd.ExcelFile('archivos_excel/descuentos_vip_csa.xlsx')
    dfCSA = efDescuentos.parse('CSA Vigentes')
    lista_csa = dfCSA.iloc[1:]
    for i in range(0, lista_csa.iloc[:, 2].count()):
        nombre = lista_csa.iloc[i, 0]
        documento = lista_csa.iloc[i, 2]
        csa = Csa(documento=int(documento), nombre=nombre)
        csa = Csa.objects.crear_csa(csa)

        tipo = TipoArticulo.objects.get(nombre="Aceites")
        aceites_ventanilla = lista_csa.iloc[i, 3]
        guardarDescuentoCSA(csa, aceites_ventanilla,
                            tipo, 'Ventanilla')
        aceites_repme = lista_csa.iloc[i, 11]
        guardarDescuentoCSA(csa, aceites_repme,
                            tipo, 'Repme')

        tipo = TipoArticulo.objects.get(nombre="Colisión")
        colision_ventanilla = lista_csa.iloc[i, 4]
        guardarDescuentoCSA(csa, colision_ventanilla,
                            tipo, 'Ventanilla')
        colision_repme = lista_csa.iloc[i, 12]
        guardarDescuentoCSA(csa, colision_repme,
                            tipo, 'Repme')

        tipo = TipoArticulo.objects.get(nombre="Cabina")
        cabinas_ventanilla = lista_csa.iloc[i, 5]
        guardarDescuentoCSA(csa, cabinas_ventanilla,
                            tipo, 'Ventanilla')
        cabinas_repme = lista_csa.iloc[i, 13]
        guardarDescuentoCSA(csa, cabinas_repme,
                            tipo, 'Repme')

        tipo = TipoArticulo.objects.get(nombre="Cummins")
        cummins_ventanilla = lista_csa.iloc[i, 6]
        guardarDescuentoCSA(csa, cummins_ventanilla,
                            tipo, 'Ventanilla')
        cummins_repme = lista_csa.iloc[i, 14]
        guardarDescuentoCSA(csa, cummins_repme, tipo, 'Repme')

        tipo = TipoArticulo.objects.get(nombre="Filtros")
        filtros_ventanilla = lista_csa.iloc[i, 7]
        guardarDescuentoCSA(csa, filtros_ventanilla, tipo, 'Ventanilla')
        filtros_repme = lista_csa.iloc[i, 15]
        guardarDescuentoCSA(csa, filtros_repme, tipo, 'Repme')

        tipo = TipoArticulo.objects.get(nombre="Llantas")
        llantas_ventanilla = lista_csa.iloc[i, 8]
        guardarDescuentoCSA(csa, llantas_ventanilla, tipo, 'Ventanilla')
        llantas_repme = lista_csa.iloc[i, 16]
        guardarDescuentoCSA(csa, llantas_repme, tipo, 'Repme')

        tipo = TipoArticulo.objects.get(nombre="Motores Diesel")
        motores_ventanilla = lista_csa.iloc[i, 9]
        guardarDescuentoCSA(csa, motores_ventanilla, tipo, 'Ventanilla')
        motores_repme = lista_csa.iloc[i, 17]
        guardarDescuentoCSA(csa, motores_repme, tipo, 'Repme')

        tipo = TipoArticulo.objects.get(nombre="Repuestos Gral")
        general_ventanilla = lista_csa.iloc[i, 10]
        guardarDescuentoCSA(csa, general_ventanilla, tipo, 'Ventanilla')
        general_repme = lista_csa.iloc[i, 18]
        guardarDescuentoCSA(csa, general_repme, tipo, 'Repme')

from django.shortcuts import render

import pandas as pd

from descuentoVIP.models import Categoria, Vip
from descuentoVIP.forms import VipForm
# Create your views here.


def visualizarVip(request):
    lista_vip = Vip.objects.all()
    form = VipForm()
    if request.method == 'POST':
        form = VipForm(request.POST)
        if form.is_valid():
            cliente = form.cleaned_data.get('cliente')
            categoria = form.cleaned_data.get('categoria')
            documento = form.cleaned_data.get('documento')
            if cliente != None:
                lista_vip = lista_vip.filter(nombre=cliente)
            if categoria != None:
                lista_vip = lista_vip.filter(categoriaVip__nombre=categoria)
            if documento != None:
                lista_vip = lista_vip.filter(documento__icontains=documento)
    return render(request, 'descuentoVIP/index.html', {'lista_vip': lista_vip, 'form': form})


def actualizarVip():
    Vip.objects.all().delete()
    Categoria.objects.all().delete()

    efVipCsa = pd.ExcelFile('archivos_excel/descuentos_vip_csa.xlsx')
    dfVip = efVipCsa.parse('VIP Vigentes')
    dfVip = dfVip.iloc[:, 2:]
    for i in range(0, dfVip.iloc[:, 0].count()):
        categoria = dfVip.iloc[i, 12]
        nombre = dfVip.iloc[i, 0]
        documento = int(dfVip.iloc[i, 2])
        aceite = dfVip.iloc[i, 3]
        colision = dfVip.iloc[i, 4]
        cabina = dfVip.iloc[i, 5]
        cummins = dfVip.iloc[i, 6]
        filtro = dfVip.iloc[i, 7]
        llanta = dfVip.iloc[i, 8]
        motor = dfVip.iloc[i, 9]
        repuestoGeneral = dfVip.iloc[i, 10]
        rutina = 0

        nuevaCategoria = Categoria(nombre=categoria, aceite=aceite, colision=colision, cabina=cabina,
                                   cummins=cummins, filtro=filtro, llanta=llanta, motor=motor, repuestoGeneral=repuestoGeneral, rutina=rutina)
        if Categoria.objects.filter(nombre=categoria).filter(aceite=aceite).filter(colision=colision).filter(cabina=cabina).filter(cummins=cummins).filter(filtro=filtro).filter(llanta=llanta).filter(motor=motor).filter(repuestoGeneral=repuestoGeneral).filter(rutina=rutina).exists():
            nuevaCategoria = Categoria.objects.filter(nombre=categoria).filter(aceite=aceite).filter(colision=colision).filter(cabina=cabina).filter(
                cummins=cummins).filter(filtro=filtro).filter(llanta=llanta).filter(motor=motor).filter(repuestoGeneral=repuestoGeneral).get(rutina=rutina)
        else:
            nuevaCategoria = Categoria.objects.crear_categoria(nuevaCategoria)

        vip = Vip(documento=documento, nombre=nombre,
                  categoriaVip=nuevaCategoria)
        vip = Vip.objects.crear_vip(vip)

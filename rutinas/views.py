from django.shortcuts import render, redirect

from .models import Rutina, Vehiculo, Articulo, TipoArticulo, FiltroSustituto
from .forms import RutinaForm

import pandas as pd


def listarRutinas():
    return Rutina.objects.all()


def visualizarRutinas(request, no_encontrados=None):
    rutinas = listarRutinas()
    if request.method == "POST":
        form = RutinaForm(request.POST)
        if form.is_valid():
            vehiculo = form.cleaned_data.get('vehiculo')
            articulo = form.cleaned_data.get('articulo')
            tipo = form.cleaned_data.get('tipo')
            if vehiculo != None:
                rutinas = rutinas.filter(vehiculo=vehiculo)
            if articulo != "":
                rutinas = rutinas.filter(articulo__ean__icontains=articulo)
            if tipo != None:
                rutinas = rutinas.filter(articulo__tipo=tipo)
    else:
        form = RutinaForm()
    return render(request, 'rutinas/index.html', {'rutinas': rutinas, 'form': form, 'no_encontrados': no_encontrados})


def actualizarRutinas():
    Rutina.objects.all().delete()
    Vehiculo.objects.all().delete()
    actualizarArticulos()
    efRutinas = pd.ExcelFile(
        'D:/Estudio/Proyecto_Ultron/archivos_excel/rutinas.xlsx')
    lista_vehiculos = efRutinas.sheet_names
    lista_articulos = Articulo.objects.all()
    lista_rutinas = listarRutinas()

    EANES_EXCLUIDOS = ["7701023403177", "7701023316132"]
    lista_no_encontrados = []
    for vehiculo in lista_vehiculos:
        if Vehiculo.objects.filter(linea=vehiculo).exists():
            vehiculoRutina = Vehiculo.objects.get(linea=vehiculo)
        else:
            vehiculoRutina = Vehiculo.objects.crear_vehiculo(vehiculo)
        rutina = efRutinas.parse(vehiculo)
        rutina = rutina[~rutina.iloc[:, 2].isna()]
        rutina.columns = list(rutina.iloc[0])
        rutina = rutina.iloc[1:, 1:]

        for i in range(0, rutina.iloc[:, 1].count()):
            if lista_articulos.filter(ean=rutina.iloc[i, 1]).exists():
                articulo = lista_articulos.get(
                    ean=rutina.iloc[i, 1])
            else:
                if str(rutina.iloc[i, 1]) not in lista_no_encontrados:
                    lista_no_encontrados.append(str(rutina.iloc[i, 1]))
                continue
            if not isinstance(rutina.iloc[i, 4], int):
                continue
            cantidad = rutina.iloc[i, 2]
            unidadIvaIncluido = rutina.iloc[i, 4]
            rutinaNueva = Rutina(vehiculo=vehiculoRutina, articulo=articulo,
                                 precioUnitario=unidadIvaIncluido, cantidad=cantidad)
            existe = lista_rutinas.filter(vehiculo=rutinaNueva.vehiculo).filter(articulo=rutinaNueva.articulo).filter(
                precioUnitario=rutinaNueva.precioUnitario).filter(cantidad=rutinaNueva.cantidad).exists()
            if existe:
                continue
            else:
                Rutina.objects.crear_rutina(rutinaNueva)
    return lista_no_encontrados


def actualizarRutinasRedirect(request):
    no_encontrados = actualizarRutinas()
    if no_encontrados != []:
        no_encontrados = ", ".join(no_encontrados)
    else:
        no_encontrados = "-"
    return redirect("visualizar_rutinas_mensaje", no_encontrados=no_encontrados)


def actualizarArticulos():
    Articulo.objects.all().delete()
    FiltroSustituto.objects.all().delete()
    TipoArticulo.objects.all().delete()
    efDescuentos = pd.ExcelFile('archivos_excel/descuentos.xlsx')
    dfArticulos = efDescuentos.parse("Filtros Rutinas")
    lista_tipos = TipoArticulo.objects.all()
    for i in range(0, dfArticulos.iloc[:, 0].count()):
        ean = dfArticulos.iloc[i, 0]
        descripcion = dfArticulos.iloc[i, 1]
        tipo = dfArticulos.iloc[i, 2]
        if lista_tipos.filter(nombre=tipo).exists():
            tipo = lista_tipos.get(nombre=tipo)
        else:
            tipo = TipoArticulo.objects.crear_tipo_articulo(tipo)
        articulo = Articulo(ean=ean, nombre=descripcion, tipo=tipo)
        articulo = Articulo.objects.crear_articulo(articulo)
    actualizarListaFiltros()


def actualizarListaFiltros():
    efDescuentos = pd.ExcelFile('archivos_excel/descuentos.xlsx')
    dfFiltrosSustitutos = efDescuentos.parse('Filtros Rutinas')
    lista_tipos = TipoArticulo.objects.all()
    for i, ean in enumerate(dfFiltrosSustitutos.iloc[:, 0]):
        nombre = dfFiltrosSustitutos.iloc[i, 1]
        tipo = dfFiltrosSustitutos.iloc[i, 2]
        if lista_tipos.filter(nombre=tipo).exists():
            tipo = lista_tipos.get(nombre=tipo)
        else:
            print('Error')
        nuevoFiltro = FiltroSustituto(ean=ean, nombre=nombre, tipo=tipo)
        nuevoFiltro = FiltroSustituto.objects.crear_filtroSustituto(
            nuevoFiltro)

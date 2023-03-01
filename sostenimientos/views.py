from django.shortcuts import render, redirect
from django.db.models import Q

import pandas as pd
from datetime import datetime

from sostenimientos.models import Factura, Articulo, Sostenimiento, Identificador, Grupo
from sostenimientos.forms import SostenimientoForm

from rutinas.models import Rutina, FiltroSustituto

from descuentoLlantas.models import Descuento

from otrosDescuentos.models import DescuentoBateria

from descuentoCSA.models import Descuento as Csa

from descuentoVIP.models import Vip

# Create your views here.


def listarSostenimientos():
    return Sostenimiento.objects.all()


def cargarDescuentosFile(pagina):
    efDescuentos = pd.ExcelFile('archivos_excel/descuentos.xlsx')
    return efDescuentos.parse(pagina)


def visualizarSostenimientos(request, msg=""):

    sostenimientos = listarSostenimientos()
    justificados = len(sostenimientos.exclude(
        Q(justificacion="Sin justificación") | Q(justificacion__icontains="NO")))
    injustificados = len(sostenimientos.filter(
        justificacion__icontains="NO"))
    pendientes = len(sostenimientos.filter(
        justificacion__icontains="Sin justificación"
    ))
    cantidad = len(sostenimientos)
    form = SostenimientoForm()
    if request.method == "POST":
        form = SostenimientoForm(request.POST)
        if form.is_valid():
            factura = form.cleaned_data.get('factura')
            ean = form.cleaned_data.get('ean')
            justificacion = form.cleaned_data.get('justificacion')
            if factura != "":
                sostenimientos = sostenimientos.filter(
                    articulo__factura__numero__icontains=factura)
            if ean != "":
                sostenimientos = sostenimientos.filter(
                    articulo__ean__icontains=ean
                )
            if justificacion == "2":
                sostenimientos = sostenimientos.exclude(
                    Q(justificacion="Sin justificación") | Q(justificacion__icontains="NO"))
            elif justificacion == "3":
                sostenimientos = sostenimientos.filter(
                    justificacion__icontains="NO")
            elif justificacion == "4":
                sostenimientos = sostenimientos.filter(
                    justificacion__icontains="Sin justificación"
                )
    return render(
        request,
        'sostenimientos/index.html',
        {
            'sostenimientos': sostenimientos,
            'form': form,
            'cantidad': cantidad,
            'injustificados': injustificados,
            'justificados': justificados,
            'pendientes': pendientes,
            'msg': msg
        })


def actualizarSostenimientos():

    Sostenimiento.objects.all().delete()
    Articulo.objects.all().delete()
    Factura.objects.all().delete()
    actualizarIdentificadores()

    lista_identificadores = Identificador.objects.all()

    dfGrupo = cargarDescuentosFile('Grupo')
    eanesConGrupo = list(dfGrupo.iloc[:, 0])
    gruposEan = list(dfGrupo.iloc[:, 1])
    efSostenimientos = pd.ExcelFile(
        'D:/Estudio/Proyecto_Ultron/archivos_excel/FOFON.xls')
    sostenimientos = efSostenimientos.parse('ReporteCambioPrecio')
    sostenimientos = sostenimientos[~sostenimientos.iloc[:, 1].isna()]
    sostenimientos.columns = list(sostenimientos.iloc[0])
    sostenimientos = sostenimientos.iloc[1:, 0:]

    CATEGORIAS_EXCLUIDAS = ["Vehiculos", "Servicios"]

    for i in range(0, sostenimientos['FECHA'].count()):
        factura = ""
        fecha = ""
        tipoDocumento = ""
        cliente = ""
        nombreCliente = ""
        ean = ""
        descripcion = ""
        observacion = ""
        cajero = ""
        cantidad = ""
        precioInicial = ""
        precioFinal = ""
        descuento = ""
        precioDescuento = ""
        sostenimientoPrecio = ""
        unidadNegocio = ""
        promocionAplicada = ""
        clasificacion = ""

        clasificacion = sostenimientos.iloc[i, 26]
        if clasificacion in CATEGORIAS_EXCLUIDAS:
            continue

        factura = sostenimientos.iloc[i, 0]
        fechaStr = sostenimientos.iloc[i, 1]
        fecha = datetime.strptime(fechaStr[:19], '%Y-%m-%d %H:%M:%S')

        tipoDocumento = sostenimientos.iloc[i, 2]
        cliente = sostenimientos.iloc[i, 3]
        cliente = cliente[2:] if "_" in cliente else cliente
        nombreCliente = sostenimientos.iloc[i, 4]
        ean = int(sostenimientos.iloc[i, 5])
        descripcion = sostenimientos.iloc[i, 6]
        observacion = sostenimientos.iloc[i, 8]
        cajero = sostenimientos.iloc[i, 10]
        cantidad = sostenimientos.iloc[i, 11]
        precioInicial = sostenimientos.iloc[i, 12]
        precioFinal = sostenimientos.iloc[i, 13]
        descuento = sostenimientos.iloc[i, 15]
        precioDescuento = sostenimientos.iloc[i, 16]
        sostenimientoPrecio = sostenimientos.iloc[i, 24]
        unidadNegocio = sostenimientos.iloc[i, 25]
        promocionAplicada = sostenimientos.iloc[i, 28]

        existeFactura = Factura.objects.filter(numero=factura).exists()
        if not existeFactura:
            facturaNueva = Factura(numero=factura, fecha=fecha, cajero=cajero, cliente=cliente, tipoDocumento=tipoDocumento,
                                   nombreCliente=nombreCliente, observacion=observacion, unidadNegocio=unidadNegocio)
            facturaNueva = Factura.objects.crear_factura(facturaNueva)
        else:
            facturaNueva = Factura.objects.get(numero=factura)

        articuloNuevo = Articulo(ean=ean, nombre=descripcion, cantidad=cantidad, precioInicial=precioInicial, precioFinal=precioFinal,
                                 descuento=descuento, precioDescuento=precioDescuento, sostenimientoPrecio=sostenimientoPrecio, promocionAplicada=promocionAplicada, factura=facturaNueva)
        articuloNuevo = Articulo.objects.crear_articulo(articuloNuevo)

        for identificador in lista_identificadores:
            if str(identificador.id) in sostenimientoPrecio:
                identificadorUsado = lista_identificadores.get(
                    id=identificador.id)
                continue

        if ean in eanesConGrupo:
            grupo = gruposEan[eanesConGrupo.index(ean)]
            grupo = Grupo.objects.get(nombre=grupo)
        else:
            grupo = Grupo.objects.get(id=1)

        sostenimiento = Sostenimiento(
            articulo=articuloNuevo, justificacion="Sin justificación", identificador=identificadorUsado, grupo=grupo)
        sostenimiento = Sostenimiento.objects.crear_sostenimiento(
            sostenimiento)


def actualizarSostenimientosRedirect(request):
    actualizarSostenimientos()
    return redirect("visualizar_sostenimientos_mensaje", msg="Lista de sostenimientos actualizadas")


def actualizarIdentificadores():
    Identificador.objects.all().delete()
    dfIdentificadores = cargarDescuentosFile('Identificadores')
    for i in range(dfIdentificadores.iloc[:, 0].count()):
        id = dfIdentificadores.iloc[i, 0][:3]
        nombre = dfIdentificadores.iloc[i, 0][5:]
        nuevoIdentificador = Identificador(id=id, nombre=nombre)
        nuevoIdentificador = Identificador.objects.crear_identificador(
            nuevoIdentificador)


def actualizarGrupo():
    Grupo.objects.all().exclude(nombre="Sin Grupo").delete()
    dfGrupo = cargarDescuentosFile('Grupo')
    for grupo in dfGrupo['GRUPO'].unique():
        Grupo.objects.crear_grupo(grupo)


def justificarSostenimientos():

    lista_sostenimientos = listarSostenimientos()
    lista_rutinas = Rutina.objects.all()
    lista_descuentosLlantas = Descuento.objects.all()
    lista_descuentosBateria = DescuentoBateria.objects.all()
    lista_filtros = FiltroSustituto.objects.all()

    criterio1 = Q(justificacion="Sin justificación")
    criterio2 = Q(justificacion__icontains="Compartir Autorización")
    criterio3 = Q(identificador__id=234)
    criterio4 = Q(identificador_id=235)

    for sostenimiento in lista_sostenimientos.filter((criterio1 | criterio2) & (criterio3 | criterio4)):
        sostenimiento.justificacion = "Compartir Autorización - NO"
        sostenimiento.save()

    for sostenimiento in lista_sostenimientos.filter(Q(articulo__descuento=0)):
        sostenimiento.justificacion = "Sostenimiento hacia arriba - OK"
        sostenimiento.save()

    for sostenimiento in lista_sostenimientos.filter(identificador__nombre__icontains="Rutina"):
        observacion = sostenimiento.articulo.factura.observacion.upper()
        if lista_filtros.filter(ean=sostenimiento.articulo.ean).exists():
            linea = ""
            if "BJ" in observacion:
                posicion = observacion.find("BJ")
                linea = observacion[posicion:(posicion+6)]
                if " " in linea:
                    linea = observacion[posicion:(posicion+7)]
                    linea.replace(" ", "")
            elif "TUNLAND" in observacion or "BJ1037" in observacion:
                linea = "BJ2037"
            elif "MINIVAN" in observacion or "MV5" in observacion or "MVP" in observacion:
                linea = "BJ5023"
            elif "MINITRUCK" in observacion:
                linea = "BJ1036"
            else:
                linea = ""
                sostenimiento.justificacion = "Rutina - Indicar la línea del vehículo - NO"
                sostenimiento.save()
                continue

            linea = "Minivan" if linea == "BJ5023" or linea == "BJ6425" else linea
            linea = "TM 2020" if linea == "BJ1030" else linea
            linea = "Minitruck" if linea == "BJ1036" else linea
            linea = "Tunland" if linea == "BJ2037" else linea

            if lista_rutinas.filter(vehiculo__linea__icontains=linea).exists():
                lista_rutinas.filter(vehiculo__linea__icontains=linea)
                if lista_rutinas.filter(precioUnitario__gte=(sostenimiento.articulo.precioFinal-100)).filter(precioUnitario__lte=(sostenimiento.articulo.precioFinal+100)).exists:
                    sostenimiento.justificacion = "Precio de rutina - OK"
                else:
                    sostenimiento.justificacion = "No coincide precio de rutina - NO"
                sostenimiento.save()

    for sostenimiento in lista_sostenimientos:
        if lista_descuentosLlantas.filter(llanta__ean=sostenimiento.articulo.ean).exists():
            descuento = lista_descuentosLlantas.get(
                llanta__ean=sostenimiento.articulo.ean)
            if descuento.porcentaje >= sostenimiento.articulo.descuento:
                sostenimiento.justificacion = "Descuento llantas - OK"
            else:
                sostenimiento.justificacion = "No coincide descuento llanta - NO"
            sostenimiento.save()

    for sostenimiento in lista_sostenimientos:
        if lista_descuentosBateria.filter(ean=sostenimiento.articulo.ean):
            descuentoBateria = lista_descuentosBateria.get(
                ean=sostenimiento.articulo.ean)
            if descuentoBateria.precioUnitario == (sostenimiento.articulo.precioFinal / sostenimiento.articulo.cantidad):
                sostenimiento.justificacion = "Precio de retoma - OK"
            else:
                sostenimiento.justificación = "No coincide precio de retoma"
            sostenimiento.save()

    lista_csa = Csa.objects.all()
    lista_vip = Vip.objects.all()
    for sostenimiento in lista_sostenimientos:
        if lista_csa.filter(csa__documento=sostenimiento.articulo.factura.cliente).exists():
            categoria = mapeoGruposCsaVip(sostenimiento.grupo.nombre)

            descuentoCsaVentanilla = lista_csa.filter(Q(csa__documento=sostenimiento.articulo.factura.cliente) & Q(
                origen="Ventanilla")).get(tipoArticulo__nombre=categoria).descuento

            descuentoCsaRepme = lista_csa.filter(Q(csa__documento=sostenimiento.articulo.factura.cliente) & Q(
                origen="Repme")).get(tipoArticulo__nombre=categoria).descuento

            if sostenimiento.articulo.descuento <= descuentoCsaVentanilla:
                sostenimiento.justificacion = "Descuento CSA Ventanilla - OK"
            elif sostenimiento.articulo.descuento <= descuentoCsaRepme:
                sostenimiento.justificacion = "Descuento CSA Repme - OK"
            else:
                sostenimiento.justificion = "No coincide descuento CSA - NO"
            sostenimiento.save()
        if lista_vip.filter(documento=sostenimiento.articulo.factura.cliente).exists():
            clienteVip = lista_vip.get(
                documento=sostenimiento.articulo.factura.cliente)
            descuentosVip = {
                "Aceites": clienteVip.categoriaVip.aceite,
                "Colisión": clienteVip.categoriaVip.colision,
                "Cabina": clienteVip.categoriaVip.cabina,
                "Cummins": clienteVip.categoriaVip.cummins,
                "Filtros": clienteVip.categoriaVip.filtro,
                "Llantas": clienteVip.categoriaVip.llanta,
                "Motores Diesel": clienteVip.categoriaVip.motor,
                "Repuestos Gral": clienteVip.categoriaVip.repuestoGeneral
            }
            categoria = mapeoGruposCsaVip(sostenimiento.grupo.nombre)
            if sostenimiento.articulo.descuento <= descuentosVip[categoria]:
                sostenimiento.justificacion = "Descuento VIP - OK"
            else:
                sostenimiento.justificacion = "No coincide descuento VIP - NO"
            sostenimiento.save()
    criterio2 = Q(articulo__factura__observacion__icontains="BJ")
    criterio3 = Q(articulo__factura__observacion__icontains="bJ")
    criterio4 = Q(articulo__factura__observacion__icontains="Bj")
    criterio5 = Q(articulo__factura__observacion__icontains="bj")

    for sostenimiento in lista_sostenimientos.filter(criterio1 & criterio2 & criterio3 & criterio4 & criterio5):
        if lista_filtros.filter(ean=sostenimiento.articulo.ean).exists():
            observacion = sostenimiento.articulo.factura.observacion.upper()
            if "BJ" in observacion:
                posicion = observacion.find("BJ")
                linea = observacion[posicion:(posicion+6)]
                if " " in linea:
                    linea = observacion[posicion:(posicion+7)]
                    linea.replace(" ", "")
            elif "TUNLAND" in observacion:
                linea = "BJ2037"

            linea = "Minivan" if linea == "BJ5023" or linea == "BJ6425" else linea
            linea = "TM 2020" if linea == "BJ1030" else linea
            linea = "Minitruck" if linea == "BJ1036" else linea
            linea = "Tunland" if linea == "BJ2037" else linea

            if lista_rutinas.filter(vehiculo__linea__icontains=linea).exists():
                lista_rutinas = lista_rutinas.filter(
                    vehiculo__linea__icontains=linea)
                if lista_rutinas.filter(precioUnitario__gte=(sostenimiento.articulo.precioFinal-100)).filter(precioUnitario__lte=(sostenimiento.articulo.precioFinal+100)).exists():
                    sostenimiento.justificacion = "Precio de rutina - OK"
                else:
                    sostenimiento.justificacion = "No coincide precio de rutina - NO"
                sostenimiento.save()

    for sostenimiento in lista_sostenimientos.filter(justificacion="Sin justificación"):
        sostenimiento.justificacion = "Compartir Autorización - NO"
        sostenimiento.save()


def justificarSostenimientosRedirect(request):
    justificarSostenimientos()
    return redirect("visualizar_sostenimientos_mensaje", msg="Lista de sostenimientos justificada")


def mapeoGruposCsaVip(categoriaBuscada):
    GRUPOS_GR = (
        ('GR_INSUMO', 'Aceites'),
        ('GR_COLISIO', 'Colisión'),
        ('GR_CABINA', 'Cabina'),
        ('GR_CUMMINS', 'Cummins'),
        ('GR_FILTRO', 'Filtros'),
        ('GR_LLANTA', 'Llantas'),
        ('GR_MOTOR', 'Motores Diesel'),
        ('GR_REPGRAL', 'Repuestos Gral')
    )
    if categoriaBuscada == "Sin Grupo":
        grupoEncontrado = 'Repuestos Gral'
    else:
        for i, grupo in enumerate(GRUPOS_GR):
            if grupo[0] == categoriaBuscada:
                grupoEncontrado = GRUPOS_GR[i][1]
                break
    return grupoEncontrado


def visualizar_factura(request, factura):

    if Factura.objects.filter(numero=factura).exists():
        datos_factura = Factura.objects.get(numero=factura)
        lista_sostenimientos = listarSostenimientos()
        articulos_de_factura = lista_sostenimientos.filter(
            articulo__factura__numero=factura)
        valor_total = 0
        for sostenimiento in articulos_de_factura:
            valor_total += sostenimiento.articulo.precioFinal
        valor_total = formatear_precio(valor_total)
    else:
        datos_factura = {"error": f"Factura {factura} no encontrada"}

    return render(request, 'sostenimientos/factura.html', {'factura': datos_factura, 'sostenimientos': articulos_de_factura, 'total': valor_total})


def formatear_precio(precio):
    precio_formateado = []
    for i, numero in enumerate(str(precio)[::-1]):
        if i == 3:
            precio_formateado.insert(0, ".")
            precio_formateado.insert(0, numero)
        elif i == 6:
            precio_formateado.insert(0, "'")
            precio_formateado.insert(0, numero)
        else:
            precio_formateado.insert(0, numero)
    precio_formateado = "".join(precio_formateado)
    return precio_formateado

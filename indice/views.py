from django.shortcuts import render, redirect
from django.http import HttpResponse

from sostenimientos.views import actualizarSostenimientos, justificarSostenimientos, UNIDADES
from sostenimientos.models import Sostenimiento
from rutinas.views import actualizarRutinas
from descuentoCSA.views import actualizarCSA
from descuentoVIP.views import actualizarVip
from descuentoLlantas.views import actualizarLlantas
from otrosDescuentos.views import actualizarOtrosDescuentos

import openpyxl
from datetime import datetime
# Create your views here.


def inicio(request, msg="", no_encontrados="-"):
    return render(request, 'indice/index.html', {'msg': msg, 'no_encontrados': no_encontrados})


def actualizar_sostenimientos(request):
    actualizarSostenimientos()
    msg = "Lista de sostenimientos actualizada"
    return redirect('inicio_mensaje', msg=msg, no_encontrados="-")


def actualizar_rutinas(request):
    no_encontrados = actualizarRutinas()
    if no_encontrados != []:
        no_encontrados = ", ".join(no_encontrados)
    else:
        no_encontrados = "-"
    msg = "Lista de rutinas actualizada"
    return redirect('inicio_mensaje', msg=msg, no_encontrados=no_encontrados)


def actualizar_csa(request):
    actualizarCSA()
    msg = "Lista de CSA actualizada"
    return redirect('inicio_mensaje', msg=msg, no_encontrados="-")


def actualizar_vip(request):
    actualizarVip()
    msg = "Lista de VIP actualizada"
    return redirect('inicio_mensaje', msg=msg, no_encontrados="-")


def actualizar_llantas(request):
    actualizarLlantas()
    msg = "Lista de llantas actualizada"
    return redirect('inicio_mensaje', msg=msg, no_encontrados="-")


def actualizar_otros_descuentos(request):
    actualizarOtrosDescuentos()
    msg = "Lista de otros descuentos actualizada"
    return redirect('inicio_mensaje', msg=msg, no_encontrados="-")


def actualizar_todo(request):
    try:
        actualizarSostenimientos()
    except:
        msg = "Error al actualizar los sostenimientos "
    try:
        no_encontrados = actualizarRutinas()
        if no_encontrados != []:
            no_encontrados = ", ".join(no_encontrados)
        else:
            no_encontrados = "-"
    except:
        error = "Error al actualizar las rutinas "
        msg = error if msg == "" else msg + error
    try:
        actualizarCSA()
    except:
        error = "Error al actualizar la lista de CSA "
        msg = error if msg == "" else msg + error

    actualizarVip()
    actualizarLlantas()
    actualizarOtrosDescuentos()
    justificarSostenimientos()

    msg = "Se actualizaron todas las listas satisfactoriamente"
    return redirect('inicio_mensaje', msg=msg, no_encontrados=no_encontrados)


def generar_informe(request):
    print("*** Inicio de generación de informe ***")
    lista_sostenimientos = Sostenimiento.objects.all()
    informe = openpyxl.Workbook()
    hoja = informe.active
    hoja.append(("Cajero", "unidadNegocio", "Fecha", "Factura", "Cliente", "Nombre Cliente", "Observacion", "EAN",
                "Descripción", "Cantidad", "Precio Inicial", "Descuento", "Precio Final", "Justificación"))
    for sostenimiento in lista_sostenimientos:
        unidadNegocio = sostenimiento.articulo.factura.unidadNegocio
        cajero = sostenimiento.articulo.factura.cajero
        fecha = sostenimiento.articulo.factura.fecha
        factura = sostenimiento.articulo.factura.numero
        cliente = sostenimiento.articulo.factura.cliente
        nombreCliente = sostenimiento.articulo.factura.nombreCliente
        observacion = sostenimiento.articulo.factura.observacion
        ean = sostenimiento.articulo.ean
        descripcion = sostenimiento.articulo.nombre
        cantidad = sostenimiento.articulo.cantidad
        precioInicial = sostenimiento.articulo.precioInicial
        descuento = sostenimiento.articulo.descuento
        precioFinal = sostenimiento.articulo.precioFinal
        justificacion = sostenimiento.justificacion
        hoja.append((cajero, unidadNegocio, fecha, factura, cliente, nombreCliente, observacion, ean, descripcion,
                    cantidad, precioInicial, descuento, precioFinal, justificacion))

    response = HttpResponse(content_type='application/msexcel')
    fecha_informe = datetime.strftime(datetime.today(), '%d-%m-%Y - %H %M %S')
    response[
        'Content-Disposition'] = f'attachment; filename = informe de sostenimientos {fecha_informe}.xlsx'
    informe.save(response)
    return response

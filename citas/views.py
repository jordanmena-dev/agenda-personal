from django.shortcuts import render
from django.http import HttpResponse
from .models import Servicio, Cita, Cliente
from django.utils import timezone

def lista_servicios(request):
    servicios = Servicio.objects.all()

    texto = ""
    for servicio in servicios:
        texto += f"{servicio.nombre} - Duracion: {servicio.duracion_min} minutos - precio: ${servicio.precio}<br>"

    return HttpResponse(texto)

def servicios_iva(request):
    servicios = Servicio.objects.all()

    texto = ""
    for servicio in servicios:
        precio_iva = round(float(servicio.precio) * 1.19)
        texto += f"{servicio.nombre} - precio: ${servicio.precio} - precio (IVA): ${precio_iva}<br>"

    return HttpResponse(texto)

def resumen(request):
    servicios = Servicio.objects.all()

    precio_max = 0
    precio_avg = 0
    suma = 0

    for servicio in servicios:
        suma += 1
        if precio_max < servicio.precio:
            precio_max = servicio.precio
        precio_avg += servicio.precio

    precio_avg = round(precio_avg / suma)

    texto = f"total de servicios: {suma} Servicio mas caro: {precio_max}<br> Promedio: {precio_avg}"
    
    return HttpResponse(texto)

def lista_citas(request):
    citas = Cita.objects.all()

    texto = ""
    for cita in citas:
        texto += f"Nombre: {cita.cliente} - servicio: {cita.servicio}- estado: {cita.estado}<br>"

    return HttpResponse(texto)

def facturados(request):
    citas = Cita.objects.all()

    facturas = 0
    for cita in citas:
        if cita.estado == "atendida":
            facturas += cita.servicio.precio

    texto = f"Total facturado es : {facturas}"

    return HttpResponse(texto)

def pendientes(request):
    citas = Cita.objects.all()

    texto = ""
    suma = 0
    for cita in citas:
        if cita.estado == 'pendiente':
            suma += 1
            texto += f"Nombre: {cita.cliente} - servicio: {cita.servicio} <br>"
    if suma < 1:
         texto = "No hay citas pendientes"
    else:
        texto += f"total pendiente: {suma}"

    return HttpResponse(texto)

def economicos(request):
    servicios = Servicio.objects.all()

    texto = ""
    umbral = 15000
    for servicio in servicios:
        if servicio.precio < umbral:
            texto += f"{servicio.nombre} - Duracion: {servicio.duracion_min} minutos - precio: ${servicio.precio}<br>"

    return HttpResponse(texto)

def estado(request, numero):
    cita = Cita.objects.get(id=numero)

    texto = ""

    if cita.estado == "pendiente":
        texto = "Su cita esta pendiente"
    elif cita.estado == "confirmada":
        texto = "Su cita esta confirmada"
    else:
        texto = "usted ya fue atendido/da"

    return HttpResponse(texto)

def detalle_cita(request, numero):
    try:
        cita = Cita.objects.get(id=numero)
    except Cita.DoesNotExist:
        return HttpResponse(f"No existe una cita con el numero {numero}")

    precio = cita.servicio.precio

    total_pagado = 0
    listado = ""
    for pago in cita.pagos.all():
        total_pagado += pago.monto
        listado += f"${pago.monto} - {pago.get_metodo_de_pago_display()}<br>"

    if listado == "":
        listado = "Sin pagos registrados<br>"

    saldo = precio - total_pagado

    texto = f"Cliente: {cita.cliente.nombre}<br>"
    texto += f"Servicio: {cita.servicio.nombre}<br>"
    texto += f"Fecha: {timezone.localtime(cita.fecha).strftime('%d/%m/%Y %H:%M')}<br>"
    texto += f"Estado: {cita.get_estado_display()}<br>"
    texto += f"Precio del servicio: ${precio}<br><br>"
    texto += f"Pagos:<br>{listado}<br>"
    texto += f"Total pagado: ${total_pagado}<br>"

    if saldo <= 0:
        texto += "La cita esta pagada"
    else:
        texto += f"Falta por pagar: ${saldo}"

    return HttpResponse(texto)

def pagado(request, numero):
    cita = Cita.objects.get(id=numero)

    total = 0
    for pago in cita.pagos.all():
        total += pago.monto

    texto = f"Cita: {cita}<br>Total pagado: ${total}"

    return HttpResponse(texto)

def duracion(request):
    citas = Cita.objects.all()

    total_minutos = 0
    for cita in citas:
        if cita.estado == 'confirmada':
            total_minutos += cita.servicio.duracion_min

    horas = total_minutos // 60
    minutos = total_minutos % 60

    texto = f"Tiempo agendado: {total_minutos} minutos<br>"
    texto += f"Equivale a {horas} horas y {minutos} minutos"

    return HttpResponse(texto)

def citas_por_cliente(request):
    clientes = Cliente.objects.all()

    texto = ""
    for cliente in clientes:
        cantidad = 0
        for cita in cliente.citas.all():
            cantidad += 1

        marca = ""
        if cantidad > 1:
            marca = " *"

        texto += f"{cliente.nombre}: {cantidad} citas{marca}<br>"

    return HttpResponse(texto)

def informe(request):
    citas = Cita.objects.all()

    total_citas = 0
    pendientes = 0
    confirmadas = 0
    atendidas = 0
    total_pagado = 0
    total_precio = 0

    for cita in citas:
        total_citas += 1
        total_precio += cita.servicio.precio

        if cita.estado == 'pendiente':
            pendientes += 1
        elif cita.estado == 'confirmada':
            confirmadas += 1
        else:
            atendidas += 1

        for pago in cita.pagos.all():
            total_pagado += pago.monto

    pendiente_de_cobro = total_precio - total_pagado

    texto = f"Total de citas: {total_citas}<br>"
    texto += f"Pendientes: {pendientes}<br>"
    texto += f"Confirmadas: {confirmadas}<br>"
    texto += f"Atendidas: {atendidas}<br>"
    texto += f"Monto total pagado: ${total_pagado}<br>"
    texto += f"Monto pendiente: ${pendiente_de_cobro}"

    return HttpResponse(texto)
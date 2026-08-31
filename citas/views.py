from django.shortcuts import render
from django.http import HttpResponse
from .models import Servicio, Cita

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
        texto += f"Nombre: {cita.cliente} - servicio: {cita.servicio} minutos - estado: {cita.estado}<br>"

    return HttpResponse(texto)

def facturados(request):
    citas = Cita.objects.all()

    facturas = 0
    for cita in citas:
        if cita.estado == "atendida":
            facturas += cita.servicio.precio

    texto = f"Total facturado es : {facturas}"

    return HttpResponse(texto)
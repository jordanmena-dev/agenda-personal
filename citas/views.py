from django.shortcuts import render
from django.http import HttpResponse
from .models import Servicio

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
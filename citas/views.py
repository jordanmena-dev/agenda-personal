from django.shortcuts import render
from django.http import HttpResponse
from .models import Servicio

def lista_servicios(request):
    servicios = Servicio.objects.all()

    texto = ""
    for servicio in servicios:
        precio_iva = round(float(servicio.precio) * 1.19)
        texto += f"{servicio.nombre} - precio: {servicio.precio} - precio (IVA): {precio_iva}<br>"

    return HttpResponse(texto)

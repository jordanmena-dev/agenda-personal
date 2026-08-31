from django.contrib import admin
from .models import Cliente, Servicio, Cita, Pago

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono')
    search_fields = ('nombre',)
    ordering = ('nombre',)

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'duracion_min')
    search_fields = ('nombre',)
    ordering = ('precio',)

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'servicio', 'estado', 'fecha', 'ultima_modificacion')
    search_fields = ('nombre',)
    ordering = ('fecha',)


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('cita', 'monto', 'metodo_de_pago', 'fecha_de_pago')
    search_fields = ('cita',)
    ordering = ('cita',)
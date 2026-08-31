from django.db import models
from django.utils import timezone

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.nombre

class Servicio(models.Model):
    nombre = models.CharField(max_length=80)
    precio = models.DecimalField(max_digits=8, decimal_places=0)
    duracion_min = models.IntegerField(default=30)

    def __str__(self):
        return self.nombre

class Cita(models.Model):

    class Estado(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        CONFIRMADA = 'confirmada', 'Confirmada'
        ATENDIDA = 'atendida', 'Atendida'
    
    #Si un cliente es borrado no debe quedar registro en la aplicacion, por la ley 21.719.
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='citas')
    #Mantiene un historial para tomar decisiones de negocio.
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT)
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.PENDIENTE)
    fecha = models.DateTimeField()
    creacion = models.DateTimeField(auto_now_add=True)
    ultima_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.cliente.nombre} - {self.servicio.nombre} - {timezone.localtime(self.fecha).strftime('%d/%m/%Y %H:%M')}"
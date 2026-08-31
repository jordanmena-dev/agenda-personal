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

class Pago(models.Model):
    class MetodoPago(models.TextChoices):
        TRANSFERENCIA = 'transferencia', 'Transferencia'
        EFECTIVO = 'efectivo', 'Efectivo'
        DEBITO = 'debito', 'Debito'
        CREDITO = 'credito', 'Credito'

    # CASCADE para cumplir la supresion del cliente (ley 21.719): al borrar
    # el cliente se eliminan sus citas y con ellas los pagos. Se asume la
    # perdida del respaldo contable. En un sistema real el pago guardaria
    # copia del monto y del servicio para sobrevivir al borrado, pero el
    # modelo de la guia exige la dependencia con Cita.    
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='pagos')
    monto = models.DecimalField(max_digits=8, decimal_places=0)
    metodo_de_pago = models.CharField(max_length=20, choices=MetodoPago.choices)
    fecha_de_pago = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cita.servicio} - {self.cita.id} - {timezone.localtime(self.fecha_de_pago).strftime('%d/%m/%Y %H:%M')}"
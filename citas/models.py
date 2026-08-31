from django.db import models

# Create your models here.

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
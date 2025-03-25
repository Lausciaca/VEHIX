from django.db import models

# Create your models here.
class Vehiculo(models.Model):
    marca = models.CharField(max_length=200, verbose_name='Marca del vehiculo', blank=False)
    modelo = models.CharField(max_length=200, verbose_name='Modelo del vehiculo', blank=False)
    patente = models.CharField(max_length=200, verbose_name='Patente del vehiculo', blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.marca + ' ' + self.modelo  # Concatenar cadenas correctamente
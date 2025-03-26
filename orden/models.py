import datetime
from django.db import models
from django.utils.timezone import now
from cliente.models import Cliente
from vehiculo.models import Vehiculo

class Orden(models.Model):
    COBERTURAS_CHOICES = [
        ('particular', 'Particular'),
        ('terceros', 'Contra terceros'),
        ('riesgo', 'Contra todo riesgo'),
        ('recupero', 'Recupero de siniestro')
    ]
    ESTADOS_CHOICES = [
        ('espera', 'Esperando ingreso'),
        ('taller', 'En el taller'),
        ('entregado', 'Entregado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Cliente', blank=False)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, verbose_name='Vehiculo', blank=False)
    imagenes = models.ImageField(upload_to='Imagenes/', verbose_name='Imagenes del vehiculo', blank=True, null=True)
    cobertura = models.CharField(max_length=50, choices=COBERTURAS_CHOICES, verbose_name='Modalidad de cobertura', blank=False)
    estado = models.CharField(max_length=50, choices=ESTADOS_CHOICES, verbose_name='Estado', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    codigo = models.CharField(max_length=20, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = 'orden'
        verbose_name_plural = 'ordenes'

    def __str__(self):
        return str(self.vehiculo) + ' de ' + str(self.cliente)

    def save(self, *args, **kwargs):
        if not self.codigo:  # Solo generar código si no existe
            año_actual = datetime.now().year
            ultimo_id = Orden.objects.count() + 1  # Sumar 1 al último ID
            self.codigo = f"ORD-{año_actual}-{ultimo_id:05d}"
        super().save(*args, **kwargs)

class ImagenVehiculo(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='imagenes_vehiculos/')

    def __str__(self):
        return f'Imagen {self.id} de {self.orden}'

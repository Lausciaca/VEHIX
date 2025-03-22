from django.db import models
from cliente.models import Cliente
from vehiculo.models import Vehiculo

# Create your models here.
class Orden(models.Model):
    MODALIDAD_CHOICES = [
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
    modalidad = models.CharField(max_length=50, choices=MODALIDAD_CHOICES, verbose_name='Modalidad de cobertura', blank=False)
    estado = models.CharField(max_length=50, choices=ESTADOS_CHOICES, verbose_name='Estado', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'orden'
        verbose_name_plural = 'ordenes'

    def __str__(self):
        return (self.marca_vehiculo + ' ' + self.modelo_vehiculo + ' de ' + self.nombre_cliente)

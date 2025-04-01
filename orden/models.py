from django.db import models
from cliente.models import Cliente
from vehiculo.models import Vehiculo
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
        
class OrdenParticular(models.Model):
    ESTADOS_CHOICES = [
        ('1', 'Presupuesto'),
        ('2', 'Enviar a cliente'),
        ('3', 'Acordar turno'),
        ('4', 'Ingresar al taller'),
        ('5', 'Entregado'),
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Cliente', blank=False)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, verbose_name='Vehiculo', blank=False)
    estado = models.CharField(max_length=50, choices=ESTADOS_CHOICES, verbose_name='Estado', blank=True, null=True)
    cobertura = 'Particular'
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    codigo = models.CharField(max_length=20, unique=True, blank=True, null=True)
    
    class Meta:
        verbose_name = 'orden particular'
        verbose_name_plural = 'ordenes particulares'

    def __str__(self):
        return f"{self.vehiculo} de {self.cliente} - Particular"

    def save(self, *args, **kwargs):
        if not self.codigo:  # Solo generar código si no existe
            ultimo_id = OrdenParticular.objects.count() + 1  # Sumar 1 al último ID
            self.codigo = f"ORD-1-{ultimo_id:05d}"
        super().save(*args, **kwargs)
        
class OrdenTerceros(models.Model):
    ESTADOS_CHOICES = [
        ('1', 'Presupuesto'),
        ('2', 'Enviar a cliente'),
        ('3', 'Acordar turno'),
        ('4', 'Ingresar al taller'),
        ('5', 'Entregado'),
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Cliente', blank=False)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, verbose_name='Vehiculo', blank=False)
    estado = models.CharField(max_length=50, choices=ESTADOS_CHOICES, verbose_name='Estado', blank=True, null=True)
    cobertura = 'Contra terceros'
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    codigo = models.CharField(max_length=20, unique=True, blank=True, null=True)
    
    class Meta:
        verbose_name = 'orden terceros'
        verbose_name_plural = 'ordenes terceros'

    def __str__(self):
        return f"{self.vehiculo} de {self.cliente} - Contra terceros"

    def save(self, *args, **kwargs):
        if not self.codigo:  # Solo generar código si no existe
            ultimo_id = OrdenTerceros.objects.count() + 1  # Sumar 1 al último ID
            self.codigo = f"ORD-2-{ultimo_id:05d}"
        super().save(*args, **kwargs)
        
class OrdenRiesgo(models.Model):
    ESTADOS_CHOICES = [
        ('1', 'Presupuesto'),
        ('2', 'Enviar a seguro'),
        ('3', 'Acordar turno'),
        ('4', 'Ingresar al taller'),
        ('5', 'Entregado'),
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Cliente', blank=False)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, verbose_name='Vehiculo', blank=False)
    estado = models.CharField(max_length=50, choices=ESTADOS_CHOICES, verbose_name='Estado', blank=True, null=True)
    cobertura = 'Todo riesgo'
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    codigo = models.CharField(max_length=20, unique=True, blank=True, null=True)
    
    class Meta:
        verbose_name = 'orden riesgo'
        verbose_name_plural = 'ordenes riesgo'

    def __str__(self):
        return f"{self.vehiculo} de {self.cliente} - Todo riesgo"

    def save(self, *args, **kwargs):
        if not self.codigo:  # Solo generar código si no existe
            ultimo_id = OrdenRiesgo.objects.count() + 1  # Sumar 1 al último ID
            self.codigo = f"ORD-3-{ultimo_id:05d}"
        super().save(*args, **kwargs)

class OrdenRecupero(models.Model):
    ESTADOS_CHOICES = [
        ('1', 'Solicitar documentacion'),
        ('2', 'Enviar carpeta'),
        ('3', 'Recibir y enviar poder firmado'),
        ('4', 'Acordar turno'),
        ('5', 'Ingresar al taller'),
        ('6', 'Entregado'),
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Cliente', blank=False)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, verbose_name='Vehiculo', blank=False)
    estado = models.CharField(max_length=50, choices=ESTADOS_CHOICES, verbose_name='Estado', blank=True, null=True)
    cobertura = 'Recupero de siniestro'
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    codigo = models.CharField(max_length=20, unique=True, blank=True, null=True)
    
    class Meta:
        verbose_name = 'orden recupero'
        verbose_name_plural = 'ordenes recuperos'

    def __str__(self):
        return f"{self.vehiculo} de {self.cliente} - Recupero de siniestro"

    def save(self, *args, **kwargs):
        if not self.codigo:  # Solo generar código si no existe
            ultimo_id = OrdenRecupero.objects.count() + 1  # Sumar 1 al último ID
            self.codigo = f"ORD-4-{ultimo_id:05d}"
        super().save(*args, **kwargs)
        
        
class ImagenVehiculo(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)  # Tipo de orden
    object_id = models.PositiveIntegerField(null=True, blank=True)  # ID de la orden específica
    orden = GenericForeignKey('content_type', 'object_id')  # Relación genérica
    imagen = models.ImageField(upload_to='imagenes_vehiculos/')

    def __str__(self):
        return f"Imagen de {self.orden}"
    
    
class Servicio(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    orden = GenericForeignKey('content_type', 'object_id')
    servicio = models.CharField(max_length=500)

    
    
class Presupuesto(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    orden = GenericForeignKey('content_type', 'object_id')
    
    created = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        unique_together = ('content_type', 'object_id')  # Para evitar múltiples presupuestos por orden
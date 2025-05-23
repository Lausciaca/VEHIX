from django.db import models
from cliente.models import Cliente
from vehiculo.models import Vehiculo
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import IntegrityError
from django.db.models import Max
        
        
        
class OrdenBase(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Cliente', blank=False)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, verbose_name='Vehiculo', blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    codigo = models.CharField(max_length=20, unique=True, blank=True, null=True)

    class Meta:
        abstract = True  # Esto hará que esta clase sea abstracta y no genere una tabla en la base de datos

    def monto_restante(self):
        presupuesto = self.obtener_presupuesto()
        if presupuesto:
            restante = presupuesto.monto - sum(pago.monto for pago in self.obtener_pagos())
            if restante <= 0:
                return 'Pago completo'
            return f"${restante:,.2f}".replace(",", ".")
        return 'No presupuestado'

    def es_entregado(self):
        return self.estado == self.ESTADOS_CHOICES[-1][0]  # Obtiene la clave del último estado

    def obtener_imagenes(self):
        content_type = ContentType.objects.get_for_model(self)
        return ImagenVehiculo.objects.filter(content_type=content_type, object_id=self.id)

    def obtener_presupuesto(self):
        content_type = ContentType.objects.get_for_model(self)
        return Presupuesto.objects.filter(content_type=content_type, object_id=self.id).first()

    def obtener_servicios(self):
        content_type = ContentType.objects.get_for_model(self)
        return Servicio.objects.filter(content_type=content_type, object_id=self.id)
    
    def obtener_pagos(self):
        content_type = ContentType.objects.get_for_model(self)
        return Pago.objects.filter(content_type=content_type, object_id=self.id)
    
    def obtener_estado_info(self):
        # Lógica para obtener los estados y el estado actual
        estados_dict = dict(self.ESTADOS_CHOICES)
        estado_actual = self.estado
        estados_lista = list(estados_dict.keys())

        try:
            index_estado_actual = estados_lista.index(estado_actual)
        except ValueError:
            index_estado_actual = None
        
        siguiente_estado = None
        anterior_estado = None
        if index_estado_actual is not None:
            if index_estado_actual + 1 < len(estados_lista):
                siguiente_estado = estados_lista[index_estado_actual + 1]
            if index_estado_actual - 1 >= 0:
                anterior_estado = estados_lista[index_estado_actual - 1]

        return estados_dict, estado_actual, siguiente_estado, anterior_estado
    


class OrdenParticular(OrdenBase):
    ESTADOS_CHOICES = [
        ('1', 'Enviar presupuesto al cliente'),
        ('2', 'Acordar turno'),
        ('3', 'Esperando ingreso'),
        ('4', 'En el taller'),
        ('5', 'Entregado'),
    ]
    estado = models.CharField(max_length=50, choices=ESTADOS_CHOICES, verbose_name='Estado', blank=True, null=True)
    cobertura = 'Particular'
    
    class Meta:
        verbose_name = 'orden particular'
        verbose_name_plural = 'ordenes particulares'

    def __str__(self):
        return f"{self.vehiculo} de {self.cliente} - Particular"

    def save(self, *args, **kwargs):
        if not self.codigo:
            for _ in range(5):
                ultimo_id = OrdenParticular.objects.aggregate(max_id=Max('id'))['max_id'] or 0
                nuevo_codigo = f"ORD-1-{ultimo_id + 1:05d}"
                if not OrdenParticular.objects.filter(codigo=nuevo_codigo).exists():
                    self.codigo = nuevo_codigo
                    break
            else:
                raise ValueError("No se pudo generar un código único")
        super().save(*args, **kwargs)
            
        
class OrdenTerceros(OrdenBase):
    ESTADOS_CHOICES = [
        ('1', 'Presupuesto'),
        ('2', 'Enviar a cliente'),
        ('3', 'Acordar turno'),
        ('4', 'En el taller'),
        ('5', 'Entregado'),
    ]
    estado = models.CharField(max_length=50, choices=ESTADOS_CHOICES, verbose_name='Estado', blank=True, null=True)
    cobertura = 'Contra terceros'
    
    class Meta:
        verbose_name = 'orden terceros'
        verbose_name_plural = 'ordenes terceros'

    def __str__(self):
        return f"{self.vehiculo} de {self.cliente} - Contra terceros"

    def save(self, *args, **kwargs):
        if not self.codigo:
            for _ in range(5):
                ultimo_id = OrdenTerceros.objects.aggregate(max_id=Max('id'))['max_id'] or 0
                nuevo_codigo = f"ORD-2-{ultimo_id + 1:05d}"
                if not OrdenTerceros.objects.filter(codigo=nuevo_codigo).exists():
                    self.codigo = nuevo_codigo
                    break
            else:
                raise ValueError("No se pudo generar un código único")
        super().save(*args, **kwargs)
        
class OrdenRiesgo(OrdenBase):
    ESTADOS_CHOICES = [
        ('1', 'Enviar presupuesto al seguro'),
        ('2', 'Esperando respuesta'),
        ('3', 'Acordar turno'),
        ('4', 'Espeando ingreso'),
        ('5', 'En el taller'),
        ('6', 'Entregado'),
    ]
    estado = models.CharField(max_length=50, choices=ESTADOS_CHOICES, verbose_name='Estado', blank=True, null=True)
    cobertura = 'Todo riesgo'
    
    class Meta:
        verbose_name = 'orden riesgo'
        verbose_name_plural = 'ordenes riesgo'

    def __str__(self):
        return f"{self.vehiculo} de {self.cliente} - Todo riesgo"

    def save(self, *args, **kwargs):
        if not self.codigo:
            for _ in range(5):
                ultimo_id = OrdenRiesgo.objects.aggregate(max_id=Max('id'))['max_id'] or 0
                nuevo_codigo = f"ORD-3-{ultimo_id + 1:05d}"
                if not OrdenRiesgo.objects.filter(codigo=nuevo_codigo).exists():
                    self.codigo = nuevo_codigo
                    break
            else:
                raise ValueError("No se pudo generar un código único")
        super().save(*args, **kwargs)

class OrdenRecupero(OrdenBase):
    ESTADOS_CHOICES = [
        ('1', 'Solicitar documentacion'),
        ('2', 'Preparar poder'),
        ('3', 'Firmar y enviar poder'),
        ('4', 'Esperando respuesta'),
        ('5', 'Acordar turno'),
        ('6', 'En el taller'),
        ('7', 'Entregado'),
    ]
    estado = models.CharField(max_length=50, choices=ESTADOS_CHOICES, verbose_name='Estado', blank=True, null=True)
    cobertura = 'Recupero de siniestro'

    
    class Meta:
        verbose_name = 'orden recupero'
        verbose_name_plural = 'ordenes recuperos'

    def __str__(self):
        return f"{self.vehiculo} de {self.cliente} - Recupero de siniestro"
    
    def save(self, *args, **kwargs):
        if not self.codigo:
            for _ in range(5):
                ultimo_id = OrdenRecupero.objects.aggregate(max_id=Max('id'))['max_id'] or 0
                nuevo_codigo = f"ORD-4-{ultimo_id + 1:05d}"
                if not OrdenRecupero.objects.filter(codigo=nuevo_codigo).exists():
                    self.codigo = nuevo_codigo
                    break
            else:
                raise ValueError("No se pudo generar un código único")
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

    @classmethod
    def crear_servicio(cls, orden, datos):
        content_type = ContentType.objects.get_for_model(orden)
        servicio = cls(content_type=content_type, object_id=orden.id, **datos)
        servicio.save()
        return servicio

    @classmethod
    def eliminar_servicio(cls, servicio):
        if servicio:
            servicio.delete()
            return True
        return False
    
class Pago(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    orden =  GenericForeignKey('content_type', 'object_id')
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    
    @classmethod
    def crear_pago(cls, orden, datos):
        content_type = ContentType.objects.get_for_model(orden)
        pago = cls(content_type=content_type, object_id=orden.id, **datos)
        pago.save()
        return pago
    @classmethod
    def eliminar_pago(cls, pago):
        if pago:
            pago.delete()
            return True
        return False

    
    
class Presupuesto(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    orden = GenericForeignKey('content_type', 'object_id')
    
    created = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)

    archivo_pdf = models.FileField(upload_to="presupuestos/", blank=True, null=True)

    class Meta:
        unique_together = ('content_type', 'object_id')  # Para evitar múltiples presupuestos por orden

    @classmethod
    def crear_presupuesto(cls, orden, datos):
        content_type = ContentType.objects.get_for_model(orden)
        
        # Verificar si ya existe un presupuesto para esta orden
        if cls.objects.filter(content_type=content_type, object_id=orden.id).exists():
            return None  # O puedes lanzar una excepción si prefieres
        
        presupuesto = cls(content_type=content_type, object_id=orden.id, **datos)
        presupuesto.save()
        return presupuesto
    
    @classmethod
    def eliminar_presupuesto(cls, orden):
        content_type = ContentType.objects.get_for_model(orden)
        presupuesto = cls.objects.filter(content_type=content_type, object_id=orden.id).first()

        if presupuesto:
            presupuesto.delete()
            return True
        return False

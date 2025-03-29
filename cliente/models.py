from django.db import models

# Create your models here.
class Cliente(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre del cliente', blank=False)
    telefono = models.CharField(max_length=200, verbose_name='Telefono del cliente', blank=False)
    email = models.EmailField(max_length=254, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
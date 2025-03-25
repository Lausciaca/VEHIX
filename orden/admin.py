from django.contrib import admin
from .models import Orden

# Register your models here.
class OrdenAdmin(admin.ModelAdmin):
    # Permite la búsqueda por ciertos campos
    search_fields = ['cliente__nombre', 'estado', 'vehiculo__modelo']

    # Permite filtrar por ciertos campos en la lista de objetos
    list_filter = ['estado', 'cobertura']

admin.site.register(Orden, OrdenAdmin)
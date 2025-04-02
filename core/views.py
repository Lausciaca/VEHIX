from django.shortcuts import render
from orden.views import obtener_todas_las_ordenes
from collections import Counter
from orden.models import *

# Create your views here.
def index(request):
    ordenes = obtener_todas_las_ordenes()
    # Ordenar las órdenes por fecha de creación (de más reciente a más antiguo)
    ordenes.sort(key=lambda x: x.created, reverse=True)

    # Obtener solo las 3 últimasordenes
    ultimas_3_ordenes = ordenes[:3]
    
    # Contar las órdenes con el estado 'En el taller'
    en_taller = sum(1 for orden in ordenes if orden.get_estado_display() == 'En el taller')

    # Contar las órdenes cuyo estado no es 'Entregado'
    activas = sum(1 for orden in ordenes if orden.get_estado_display() != 'Entregado')
   
    
    cobertura_mas_elegida = obtener_cobertura_mas_repetida()

    return render(request, 'core/index.html', { 
        'ordenes': ultimas_3_ordenes, 
        'ordenesActivas' : activas,
        'vehiculosTaller' : en_taller,
        'coberturaMasElegida' : cobertura_mas_elegida
    })
    
    
    
def obtener_cobertura_mas_repetida():
    # Recuperar todas las órdenes
    ordenes_particulares = OrdenParticular.objects.all()
    ordenes_terceros = OrdenTerceros.objects.all()
    ordenes_riesgo = OrdenRiesgo.objects.all()
    ordenes_recupero = OrdenRecupero.objects.all()

    # Asignar las coberturas a cada tipo de orden
    coberturas = (
        ['Particular'] * len(ordenes_particulares) +
        ['Contra terceros'] * len(ordenes_terceros) +
        ['Todo riesgo'] * len(ordenes_riesgo) +
        ['Recupero de siniestro'] * len(ordenes_recupero)
    )

    # Contar las frecuencias de cada cobertura
    contador_coberturas = Counter(coberturas)

    # Obtener la cobertura más repetida
    cobertura_mas_repetida = contador_coberturas.most_common(1)

    # Si existe alguna cobertura, devolver solo el texto de la cobertura más repetida
    if cobertura_mas_repetida:
        return cobertura_mas_repetida[0][0]  # Retorna solo el nombre de la cobertura más repetida
    else:
        return None
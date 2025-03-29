from django.shortcuts import render
from orden.views import obtener_todas_las_ordenes
# from orden.models import Orden

# Create your views here.
def index(request):
    ordenes = obtener_todas_las_ordenes()
    # Ordenar las órdenes por fecha de creación (de más reciente a más antiguo)
    ordenes.sort(key=lambda x: x.created, reverse=True)

    # Obtener solo las 3 últimasordenes
    ultimas_3_ordenes = ordenes[:3]
    
    # Contar las órdenes con el estado 'En el taller'
    en_taller = sum(1 for orden in ordenes if orden.get_estado_display() == 'Ingresar al taller')

    # Contar las órdenes cuyo estado no es 'Entregado'
    activas = sum(1 for orden in ordenes if orden.get_estado_display() != 'Entregado')
    # ordenes = Orden.objects.all().order_by('-created')[:3]
    # ordenesActivas = Orden.objects.exclude(estado='entregado').count()
    # vehiculosTaller = Orden.objects.filter(estado='taller').count()

    return render(request, 'core/index.html', { 
        'ordenes': ultimas_3_ordenes, 
        'ordenesActivas' : activas,
        'vehiculosTaller' : en_taller
    })
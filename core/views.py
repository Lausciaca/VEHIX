from django.shortcuts import render
# from orden.models import Orden

# Create your views here.
def index(request):
    # ordenes = Orden.objects.all().order_by('-created')[:3]
    # ordenesActivas = Orden.objects.exclude(estado='entregado').count()
    # vehiculosTaller = Orden.objects.filter(estado='taller').count()

    return render(request, 'core/index.html', { 
        # 'ordenes': ordenes, 
        # 'ordenesActivas' : ordenesActivas,
        # 'vehiculosTaller' : vehiculosTaller
    })
from django.shortcuts import render
from .models import Orden
from cliente.models import Cliente
from vehiculo.models import Vehiculo
from .forms import OrdenSearchForm
from django.http import JsonResponse



def ordenes(request):
    # Inicializa el formulario con los parámetros GET
    form = OrdenSearchForm(request.GET)
    
    # Obtén todas las órdenes inicialmente
    ordenes = Orden.objects.all()

    # Aplica los filtros si el formulario es válido
    if form.is_valid():
        # Filtra por estado si se ha seleccionado
        if form.cleaned_data['estado']:
            ordenes = ordenes.filter(estado=form.cleaned_data['estado'])
        
        # Filtra por cobertura si se ha seleccionado
        if form.cleaned_data['cobertura']:
            ordenes = ordenes.filter(cobertura=form.cleaned_data['cobertura'])

        # Filtra por cliente si se ha proporcionado el nombre
        if form.cleaned_data['cliente']:
            ordenes = ordenes.filter(cliente__nombre__icontains=form.cleaned_data['cliente'])

        # Filtra por vehículo si se ha proporcionado el modelo
        if form.cleaned_data['vehiculo']:
            ordenes = ordenes.filter(vehiculo__modelo__icontains=form.cleaned_data['vehiculo'])

    return render(request, 'orden/ordenes.html', {
        'ordenes': ordenes,
        'form': form,
    })


def crear_orden(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.POST['nombre']
        telefono = request.POST['telefono']
        email = request.POST['email']
        marca = request.POST['marca']
        modelo = request.POST['modelo']
        patente = request.POST['patente']
        cobertura = request.POST['cobertura']
        estado = request.POST['estado']
        imagenes = request.FILES.getlist('imagenes')

        # Crear el usuario, vehículo y orden
        cliente = Cliente.objects.create(nombre=nombre, telefono=telefono, email=email)
        vehiculo = Vehiculo.objects.create(marca=marca, modelo=modelo, patente=patente, usuario=usuario)
        orden = Orden.objects.create(cobertura=cobertura, estado=estado, vehiculo=vehiculo)

        # Subir las imágenes si es necesario
        for imagen in imagenes:
            orden.imagenes.create(imagen=imagen)

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})
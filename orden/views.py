from .models import Orden, ImagenVehiculo
from .forms import OrdenSearchForm
from django.shortcuts import render, redirect
from .forms import OrdenForm, ImagenVehiculoForm
from cliente.forms import ClienteForm
from vehiculo.forms import VehiculoForm
from datetime import datetime


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


        if form.cleaned_data['search']:
            ordenes = ordenes.filter(
                vehiculo__modelo__icontains=form.cleaned_data['search']
            ) | ordenes.filter(
                vehiculo__marca__icontains=form.cleaned_data['search']
            ) | ordenes.filter(
                cliente__nombre__icontains=form.cleaned_data['search']
            )


    return render(request, 'orden/ordenes.html', {
        'ordenes': ordenes,
        'form': form,
    })




def crear_orden(request):
    if request.method == 'POST':
        # Instanciamos todos los formularios
        cliente_form = ClienteForm(request.POST)
        vehiculo_form = VehiculoForm(request.POST)
        orden_form = OrdenForm(request.POST)
        imagen_form = ImagenVehiculoForm(request.POST, request.FILES)

        # Validamos todos los formularios
        if cliente_form.is_valid() and vehiculo_form.is_valid() and orden_form.is_valid() and imagen_form.is_valid():
            # 1️⃣ Crear Cliente
            cliente = cliente_form.save()

            # 2️⃣ Crear Vehículo
            vehiculo = vehiculo_form.save()

            # 3️⃣ Crear la Orden (sin necesidad de generar el código manualmente)
            orden = orden_form.save(commit=False)
            orden.cliente = cliente
            orden.vehiculo = vehiculo
            orden.save()  # El código se genera automáticamente al guardar

            # 4️⃣ Guardar imágenes asociadas a la orden
            if 'imagen' in request.FILES:
                for img in request.FILES.getlist('imagen'):
                    ImagenVehiculo.objects.create(orden=orden, imagen=img)

            return redirect('ordenes')  # Redirige a la lista de órdenes

    else:
        # Si no es un POST, instanciamos formularios vacíos
        cliente_form = ClienteForm()
        vehiculo_form = VehiculoForm()
        orden_form = OrdenForm()
        imagen_form = ImagenVehiculoForm()

    return render(request, 'orden/crear_orden.html', {
        'cliente_form': cliente_form,
        'vehiculo_form': vehiculo_form,
        'orden_form': orden_form,
        'imagen_form': imagen_form,
    })
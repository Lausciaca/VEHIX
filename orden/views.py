from .models import Orden, ImagenVehiculo
from .forms import OrdenSearchForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import OrdenForm, ImagenVehiculoForm
from cliente.forms import ClienteForm
from vehiculo.forms import VehiculoForm
from django.contrib import messages


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
        cliente_form = ClienteForm(request.POST)
        vehiculo_form = VehiculoForm(request.POST)
        orden_form = OrdenForm(request.POST)
        imagen_form = ImagenVehiculoForm(request.POST, request.FILES)

        if cliente_form.is_valid() and vehiculo_form.is_valid() and orden_form.is_valid():
            # Crear cliente
            cliente = cliente_form.save()

            # Crear vehículo
            vehiculo = vehiculo_form.save()

            # Crear orden
            orden = orden_form.save(commit=False)
            orden.cliente = cliente
            orden.vehiculo = vehiculo
            orden.save()

            # Guardar imágenes de vehículo (manejo de múltiples archivos)
            for img in request.FILES.getlist('imagen'):  # Iterar sobre las imágenes
                ImagenVehiculo.objects.create(orden=orden, imagen=img)

            return redirect('orden:list')  # Redirigir a alguna página de éxito

    else:
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


def ver_orden(request, codigo):
    
    orden = get_object_or_404(Orden, codigo=codigo)
    imagenes = orden.imagenes_vehiculo.all()
    
    return render(request, 'orden/ver_orden.html', {'orden':orden, 'imagenes':imagenes})


def eliminar_orden(request, codigo):
    try:
        # Obtener la orden por código
        orden = Orden.objects.get(codigo=codigo)

        # Eliminar la orden
        orden.delete()

        # Mensaje de éxito
        messages.success(request, f"La orden {codigo} ha sido eliminada con éxito.")

    except Orden.DoesNotExist:
        # Si la orden no existe
        messages.error(request, "La orden que intentas eliminar no existe.")

    # Redirigir a una página de lista o donde se gestione la visualización de las órdenes
    return redirect('orden:list')  # Reemplaza 'ordenes_lista' con el nombre de la vista de lista de órdenes
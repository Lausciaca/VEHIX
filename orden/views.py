from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from cliente.forms import ClienteForm
from vehiculo.forms import VehiculoForm
from .forms import *
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages


def obtener_todas_las_ordenes():
    # Recuperar todas las órdenes de cada tipo
    ordenes_particulares = OrdenParticular.objects.all()
    ordenes_terceros = OrdenTerceros.objects.all()
    ordenes_riesgo = OrdenRiesgo.objects.all()
    ordenes_recupero = OrdenRecupero.objects.all()

    # Combinar todas las órdenes en una lista
    todas_las_ordenes = list(ordenes_particulares) + list(ordenes_terceros) + list(ordenes_riesgo) + list(ordenes_recupero)

    return todas_las_ordenes

def ordenes(request):
    todas_las_ordenes = obtener_todas_las_ordenes()
    return render(request, 'orden/ordenes.html', {'ordenes': todas_las_ordenes})





def crear_orden(request):
    if 'particular' in request.GET:
        if request.method == 'POST':
            cliente_form = ClienteForm(request.POST)
            vehiculo_form = VehiculoForm(request.POST)
            orden_form = OrdenParticularForm(request.POST)
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
                orden.estado = '1'
                orden.save()

                # Guardar imágenes de vehículo (manejo de múltiples archivos)
                for img in request.FILES.getlist('imagen'):  # Iterar sobre las imágenes
                    ImagenVehiculo.objects.create(orden=orden, imagen=img)

                return redirect('orden:list')  # Redirigir a alguna página de éxito

        else:
            cliente_form = ClienteForm()
            vehiculo_form = VehiculoForm()
            orden_form = OrdenParticularForm()
            imagen_form = ImagenVehiculoForm()

        return render(request, 'orden/crear_orden.html', {
            'cliente_form': cliente_form,
            'vehiculo_form': vehiculo_form,
            'orden_form': orden_form,
            'imagen_form': imagen_form,
        })
    
    elif 'terceros' in request.GET:
        if request.method == 'POST':
            cliente_form = ClienteForm(request.POST)
            vehiculo_form = VehiculoForm(request.POST)
            orden_form = OrdenTercerosForm(request.POST)
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
                orden.estado = '1'
                orden.save()

                # Guardar imágenes de vehículo (manejo de múltiples archivos)
                for img in request.FILES.getlist('imagen'):  # Iterar sobre las imágenes
                    ImagenVehiculo.objects.create(orden=orden, imagen=img)

                return redirect('orden:list')  # Redirigir a alguna página de éxito

        else:
            cliente_form = ClienteForm()
            vehiculo_form = VehiculoForm()
            orden_form = OrdenTercerosForm()
            imagen_form = ImagenVehiculoForm()

        return render(request, 'orden/crear_orden.html', {
            'cliente_form': cliente_form,
            'vehiculo_form': vehiculo_form,
            'orden_form': orden_form,
            'imagen_form': imagen_form,
        })
    
    elif 'riesgo' in request.GET:
        if request.method == 'POST':
            cliente_form = ClienteForm(request.POST)
            vehiculo_form = VehiculoForm(request.POST)
            orden_form = OrdenRiesgoForm(request.POST)
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
                orden.estado = '1'
                orden.save()

                # Guardar imágenes de vehículo (manejo de múltiples archivos)
                for img in request.FILES.getlist('imagen'):  # Iterar sobre las imágenes
                    ImagenVehiculo.objects.create(orden=orden, imagen=img)

                return redirect('orden:list')  # Redirigir a alguna página de éxito

        else:
            cliente_form = ClienteForm()
            vehiculo_form = VehiculoForm()
            orden_form = OrdenRiesgoForm()
            imagen_form = ImagenVehiculoForm()

        return render(request, 'orden/crear_orden.html', {
            'cliente_form': cliente_form,
            'vehiculo_form': vehiculo_form,
            'orden_form': orden_form,
            'imagen_form': imagen_form,
        })
        
    elif 'recupero' in request.GET:
        if request.method == 'POST':
            cliente_form = ClienteForm(request.POST)
            vehiculo_form = VehiculoForm(request.POST)
            orden_form = OrdenRecuperoForm(request.POST)
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
                orden.estado = '1'
                orden.save()

                # Guardar imágenes de vehículo (manejo de múltiples archivos)
                for img in request.FILES.getlist('imagen'):  # Iterar sobre las imágenes
                    ImagenVehiculo.objects.create(orden=orden, imagen=img)

                return redirect('orden:list')  # Redirigir a alguna página de éxito

        else:
            cliente_form = ClienteForm()
            vehiculo_form = VehiculoForm()
            orden_form = OrdenRecuperoForm()
            imagen_form = ImagenVehiculoForm()

        return render(request, 'orden/crear_orden.html', {
            'cliente_form': cliente_form,
            'vehiculo_form': vehiculo_form,
            'orden_form': orden_form,
            'imagen_form': imagen_form,
        })
    
    else:
        return render(request, 'orden/elegir-cobertura.html')


def ver_orden(request, codigo):

    tipo_orden = codigo.split('-')[1]
    
    orden = None
    estados = None
    
    if tipo_orden == '1':
        orden = OrdenParticular.objects.filter(codigo=codigo).first()
        estados = OrdenParticular.ESTADOS_CHOICES
    elif tipo_orden == '2':
        orden = OrdenTerceros.objects.filter(codigo=codigo).first()
        estados = OrdenTerceros.ESTADOS_CHOICES
    elif tipo_orden == '3':
        orden = OrdenRiesgo.objects.filter(codigo=codigo).first()
        estados = OrdenRiesgo.ESTADOS_CHOICES
    elif tipo_orden == '4':
        orden = OrdenRecupero.objects.filter(codigo=codigo).first()
        estados = OrdenRecupero.ESTADOS_CHOICES
        
    if not orden:
        return render(request, 'error.html', {'message': 'Orden no encontrada'})
    
    # Obtener el ContentType de la orden específica
    content_type = ContentType.objects.get_for_model(orden)
    
    # Recuperar las imágenes asociadas con la orden mediante GenericForeignKey
    imagenes = ImagenVehiculo.objects.filter(content_type=content_type, object_id=orden.id)
    
    estados_dict = dict(estados)
    estado_actual = orden.estado
    estados_lista = list(estados_dict.keys())  # Lista de los códigos de estado
    
    try:
        index_estado_actual = estados_lista.index(estado_actual)
    except ValueError:
        index_estado_actual = None
        
    # Obtener el siguiente y anterior estado, si existen
    siguiente_estado = None
    anterior_estado = None
    if index_estado_actual is not None:
        if index_estado_actual + 1 < len(estados_lista):
            siguiente_estado = estados_lista[index_estado_actual + 1]
        if index_estado_actual - 1 >= 0:
            anterior_estado = estados_lista[index_estado_actual - 1]
    
    return render(request, 'orden/ver_orden.html', {
        'orden':orden,
        'imagenes':imagenes,
        'estados_dict': estados_dict,
        'estado_actual': estado_actual,
        'siguiente_estado': siguiente_estado,
        'anterior_estado': anterior_estado,
        })


def cambiar_estado(request, codigo, estado):
    tipo_orden = codigo.split('-')[1]

    modelos = {
        '1': OrdenParticular,
        '2': OrdenTerceros,
        '3': OrdenRiesgo,
        '4': OrdenRecupero,
    }

    modelo = modelos.get(tipo_orden)
    if not modelo:
        return JsonResponse({'success': False, 'error': 'Tipo de orden inválido'}, status=400)

    orden = get_object_or_404(modelo, codigo=codigo)
    orden.estado = estado
    orden.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Genera el HTML para el timeline
        timeline_html = render_to_string("orden/timeline.html", {"orden": orden})
        return JsonResponse({'success': True, 'timeline': timeline_html, 'estado': estado})  # Enviamos el HTML actualizado
    
    return redirect('orden:detail', codigo=codigo)

def eliminar_orden(request, codigo):
    tipo_orden = codigo.split('-')[1]
    
    orden = None
    
    if tipo_orden == '1':
        orden = OrdenParticular.objects.filter(codigo=codigo).first()
    elif tipo_orden == '2':
        orden = OrdenTerceros.objects.filter(codigo=codigo).first()
    elif tipo_orden == '3':
        orden = OrdenRiesgo.objects.filter(codigo=codigo).first()
    elif tipo_orden == '4':
        orden = OrdenRecupero.objects.filter(codigo=codigo).first()
        
        
    try:
        # Eliminar la orden
        orden.delete()

        # Mensaje de éxito
        messages.success(request, f"La orden {codigo} ha sido eliminada con éxito.")

    except orden.DoesNotExist:
        # Si la orden no existe
        messages.error(request, "La orden que intentas eliminar no existe.")

    # Redirigir a una página de lista o donde se gestione la visualización de las órdenes
    return redirect('orden:list')  # Reemplaza 'ordenes_lista' con el nombre de la vista de lista de órdenes
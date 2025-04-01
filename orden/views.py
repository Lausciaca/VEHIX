from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from cliente.forms import ClienteForm
from vehiculo.forms import VehiculoForm
from .forms import *
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import HttpResponse
import io
import os
from django.conf import settings
from django.http import HttpResponse
from .filler import rellenar_pdf    
from django.http import FileResponse
    

def obtener_orden(codigo):
        tipo_orden = codigo.split('-')[1]
        
        if tipo_orden == '1':
            orden = OrdenParticular.objects.filter(codigo=codigo).first()
        elif tipo_orden == '2':
            orden = OrdenTerceros.objects.filter(codigo=codigo).first()
        elif tipo_orden == '3':
            orden = OrdenRiesgo.objects.filter(codigo=codigo).first()
        elif tipo_orden == '4':
            orden = OrdenRecupero.objects.filter(codigo=codigo).first()
        else:
            orden = None
        
        return orden
    
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
    form = OrdenSearchForm(request.GET)
    ordenes = obtener_todas_las_ordenes()  # Esto devuelve una lista, no un QuerySet

    if form.is_valid() and form.cleaned_data['search']:
        search_term = form.cleaned_data['search'].lower()

        # Filtramos manualmente la lista usando list comprehension
        ordenes = [
            orden for orden in ordenes
            if search_term in orden.vehiculo.modelo.lower()
            or search_term in orden.vehiculo.marca.lower()
            or search_term in orden.cliente.nombre.lower()
        ]

    return render(request, 'orden/ordenes.html', {'ordenes': ordenes})



def crear_orden(request):
    # Determinar el tipo de orden
    tipo_orden = None
    if 'particular' in request.GET:
        tipo_orden = 'Particular'
        orden_form_class = OrdenParticularForm
    elif 'terceros' in request.GET:
        tipo_orden = 'Terceros'
        orden_form_class = OrdenTercerosForm
    elif 'riesgo' in request.GET:
        tipo_orden = 'Riesgo'
        orden_form_class = OrdenRiesgoForm
    elif 'recupero' in request.GET:
        tipo_orden = 'Recupero'
        orden_form_class = OrdenRecuperoForm
    else:
        return render(request, 'orden/elegir-cobertura.html')

    if request.method == 'POST':
        # Crear formularios
        cliente_form = ClienteForm(request.POST)
        vehiculo_form = VehiculoForm(request.POST)
        orden_form = orden_form_class(request.POST)
        imagen_form = ImagenVehiculoForm(request.POST, request.FILES)

        if cliente_form.is_valid() and vehiculo_form.is_valid() and orden_form.is_valid():
            # Crear cliente y vehículo
            cliente = cliente_form.save()
            vehiculo = vehiculo_form.save()

            # Crear orden
            orden = orden_form.save(commit=False)
            orden.cliente = cliente
            orden.vehiculo = vehiculo
            orden.estado = '1'  # El estado predeterminado
            orden.save()

            # Guardar imágenes de vehículo (manejo de múltiples archivos)
            for img in request.FILES.getlist('imagen'):
                ImagenVehiculo.objects.create(orden=orden, imagen=img)

            return redirect('orden:list')  # Redirigir a alguna página de éxito
    else:
        # Inicializar los formularios vacíos
        cliente_form = ClienteForm()
        vehiculo_form = VehiculoForm()
        orden_form = orden_form_class()
        imagen_form = ImagenVehiculoForm()

    return render(request, 'orden/crear_orden.html', {
        'cliente_form': cliente_form,
        'vehiculo_form': vehiculo_form,
        'orden_form': orden_form,
        'imagen_form': imagen_form,
    })



def ver_orden(request, codigo):
    orden = obtener_orden(codigo)

    if not orden:
        return render(request, 'error.html', {'message': 'Orden no encontrada'})

    # Obtener imágenes, servicios y presupuesto a través de los métodos del modelo
    imagenes = orden.obtener_imagenes()
    servicios = orden.obtener_servicios()
    presupuesto = orden.obtener_presupuesto()
    pagos = orden.obtener_pagos()

    # Calcular el total pagado
    total_pagado = sum(pago.monto for pago in pagos)

    # Calcular el monto restante
    monto_restante = presupuesto.monto - total_pagado if presupuesto else 0
    
    
    # Obtener la información de los estados directamente desde el modelo
    estados_dict, estado_actual, siguiente_estado, anterior_estado = orden.obtener_estado_info()

    return render(request, 'orden/ver_orden.html', {
        'orden': orden,
        'imagenes': imagenes,
        'servicios': servicios,
        'pagos': pagos,
        'estados_dict': estados_dict,
        'estado_actual': estado_actual,
        'siguiente_estado': siguiente_estado,
        'anterior_estado': anterior_estado,
        'presupuesto': presupuesto,
        'monto_restante': monto_restante  # Pasamos el dato al template
    })


def cambiar_estado(request, codigo, estado):
    orden = obtener_orden(codigo)
    orden.estado = estado
    orden.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Genera el HTML para el timeline
        timeline_html = render_to_string("orden/timeline.html", {"orden": orden})
        return JsonResponse({'success': True, 'timeline': timeline_html, 'estado': estado})  # Enviamos el HTML actualizado
    
    return redirect('orden:detail', codigo=codigo)

def eliminar_orden(request, codigo):
    orden = obtener_orden(codigo)
    
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


# Servicio
def crear_servicio(request, codigo):
    orden = obtener_orden(codigo)

    if request.method == 'POST':
        form = CrearServicioForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data  # Obtienes los datos del formulario
            servicio = Servicio.crear_servicio(orden, form_data)
            messages.success(request, 'Servicio creado exitosamente')
            return redirect('orden:detail', codigo=codigo)
    else:
        form = CrearServicioForm()

    return render(request, 'orden/crear_servicio.html', {'form': form, 'orden': orden})
def eliminar_servicio(request, codigo, servicio_id):
    try:
        servicio = Servicio.objects.get(id=servicio_id)  # Obtener la instancia
        codigo = servicio.orden.codigo  # Obtener el código de la orden (asegúrate de que `orden` tenga un campo `codigo`)
        Servicio.eliminar_servicio(servicio)  # Llamar al método correctamente
        return redirect('orden:detail', codigo=codigo)
    except Servicio.DoesNotExist:
        return JsonResponse({"error": "Servicio no encontrado"}, status=404)


# Pago
def crear_pago(request, codigo):
    orden = obtener_orden(codigo)

    if request.method == 'POST':
        form = CrearPagoForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data  # Obtienes los datos del formulario
            pago = Pago.crear_pago(orden, form_data)
            messages.success(request, 'Pago creado exitosamente')
            return redirect('orden:detail', codigo=codigo)
    else:
        form = CrearPagoForm()

    return render(request, 'orden/crear_pago.html', {'form': form, 'orden': orden})
def eliminar_pago(request, codigo, pago_id):
    try:
        pago = Pago.objects.get(id=pago_id)  # Obtener la instancia
        codigo = pago.orden.codigo  # Obtener el código de la orden (asegúrate de que `orden` tenga un campo `codigo`)
        Pago.eliminar_pago(pago)  # Llamar al método correctamente
        return redirect('orden:detail', codigo=codigo)
    except Pago.DoesNotExist:
        return JsonResponse({"error": "Pago no encontrado"}, status=404)


# Presupuesto
def crear_presupuesto(request, codigo):
    orden = obtener_orden(codigo)
    
    if request.method == 'POST':
        form = CrearPresupuestoForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data  # Obtienes los datos del formulario
            presupuesto = Presupuesto.crear_presupuesto(orden, form_data)
            
            if presupuesto is None:
                messages.warning(request, 'Esta orden ya tiene un presupuesto asociado')
                return redirect('orden:detail', codigo=codigo)

            messages.success(request, 'Presupuesto creado exitosamente')
            return redirect('orden:detail', codigo=codigo)
    else:
        form = CrearPresupuestoForm()
    
    return render(request, 'orden/crear_presupuesto.html', {'form': form, 'orden': orden})
def eliminar_presupuesto(request, codigo):
    orden = obtener_orden(codigo)
    
    if Presupuesto.eliminar_presupuesto(orden):
        messages.success(request, "El presupuesto ha sido eliminado con éxito.")
    else:
        messages.error(request, "El presupuesto que intentas eliminar no existe.")
    
    return redirect('orden:detail', codigo=codigo)

def generar_pdf_presupuesto(request, codigo, presupuesto_id):
    # Obtener el presupuesto
    presupuesto = get_object_or_404(Presupuesto, id=presupuesto_id)
    orden = obtener_orden(codigo)

    # Si no tiene un PDF guardado, generarlo
    if not presupuesto.archivo_pdf:
        pdf_url = rellenar_pdf(orden, presupuesto)
    else:
        pdf_url = presupuesto.archivo_pdf.url

    # Devolver el PDF como respuesta de descarga
    return FileResponse(open(presupuesto.archivo_pdf.path, "rb"), as_attachment=True, filename=os.path.basename(presupuesto.archivo_pdf.path))
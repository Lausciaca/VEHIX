from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from cliente.forms import ClienteForm
from vehiculo.forms import VehiculoForm
from .forms import *
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
import fitz  # PyMuPDF
from django.http import HttpResponse
import io


from itertools import chain

def tiene_presupuesto(orden):
    content_type = ContentType.objects.get_for_model(orden)
    return Presupuesto.objects.filter(
        content_type=content_type,
        object_id=orden.id
    ).exists()
    
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
    presupuesto = None
    
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
    servicios = Servicio.objects.filter(content_type=content_type, object_id=orden.id)
    presupuesto = Presupuesto.objects.filter(content_type=content_type, object_id=orden.id).first()
    
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
        'servicios':servicios,
        'estados_dict': estados_dict,
        'estado_actual': estado_actual,
        'siguiente_estado': siguiente_estado,
        'anterior_estado': anterior_estado,
        'presupuesto': presupuesto
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


def crear_servicio(request, codigo):
    # Determinar el tipo de orden basado en el código
    tipo_orden = codigo.split('-')[1]
    
    # Mapeo de tipos de orden a modelos
    modelos_orden = {
        '1': OrdenParticular,
        '2': OrdenTerceros,
        '3': OrdenRiesgo,
        '4': OrdenRecupero,
    }
    
    # Obtener el modelo correcto
    modelo_orden = modelos_orden.get(tipo_orden)
    if not modelo_orden:
        messages.error(request, 'Tipo de orden no válido')
        return redirect('orden:list')
    
    # Obtener la orden específica
    orden = get_object_or_404(modelo_orden, codigo=codigo)
    
    # Verificar si ya existe un presupuesto para esta orden
    content_type = ContentType.objects.get_for_model(orden)
    
    if request.method == 'POST':
        form = CrearServicioForm(request.POST)
        if form.is_valid():
            servicio = form.save(commit=False)
            servicio.content_type = content_type
            servicio.object_id = orden.id
            servicio.save()
            messages.success(request, 'Servicio creado exitosamente')
            return redirect('orden:detail', codigo=codigo)
    else:
        form = CrearServicioForm()
    
    return render(request, 'orden/crear_servicio.html', {
        'form': form,
        'orden': orden
    })

def crear_presupuesto(request, codigo):
    # Determinar el tipo de orden basado en el código
    tipo_orden = codigo.split('-')[1]
    
    # Mapeo de tipos de orden a modelos
    modelos_orden = {
        '1': OrdenParticular,
        '2': OrdenTerceros,
        '3': OrdenRiesgo,
        '4': OrdenRecupero,
    }
    
    # Obtener el modelo correcto
    modelo_orden = modelos_orden.get(tipo_orden)
    if not modelo_orden:
        messages.error(request, 'Tipo de orden no válido')
        return redirect('orden:list')
    
    # Obtener la orden específica
    orden = get_object_or_404(modelo_orden, codigo=codigo)
    
    # Verificar si ya existe un presupuesto para esta orden
    content_type = ContentType.objects.get_for_model(orden)
    if Presupuesto.objects.filter(content_type=content_type, object_id=orden.id).exists():
        messages.warning(request, 'Esta orden ya tiene un presupuesto asociado')
        return redirect('orden:detail', codigo=codigo)
    
    if request.method == 'POST':
        form = CrearPresupuestoForm(request.POST)
        if form.is_valid():
            presupuesto = form.save(commit=False)
            presupuesto.content_type = content_type
            presupuesto.object_id = orden.id
            presupuesto.save()
            messages.success(request, 'Presupuesto creado exitosamente')
            return redirect('orden:detail', codigo=codigo)
    else:
        form = CrearPresupuestoForm()
    
    return render(request, 'orden/crear_presupuesto.html', {
        'form': form,
        'orden': orden
    })

def eliminar_presupuesto(request, codigo):
    # Determinar el tipo de orden basado en el código
    tipo_orden = codigo.split('-')[1]
    
    # Mapeo de tipos de orden a modelos
    modelos_orden = {
        '1': OrdenParticular,
        '2': OrdenTerceros,
        '3': OrdenRiesgo,
        '4': OrdenRecupero,
    }
    
    # Obtener el modelo correcto
    modelo_orden = modelos_orden.get(tipo_orden)
    if not modelo_orden:
        messages.error(request, 'Tipo de orden no válido')
        return redirect('orden:list')
    
    # Obtener la orden específica
    orden = get_object_or_404(modelo_orden, codigo=codigo)
    
    # Verificar si ya existe un presupuesto para esta orden
    content_type = ContentType.objects.get_for_model(orden)
    presupuesto = Presupuesto.objects.filter(content_type=content_type, object_id=orden.id)
    
    try:
        # Eliminar el presupuesto
        presupuesto.delete()

        # Mensaje de éxito
        messages.success(request, "El presupuesto ha sido eliminado con éxito.")
    
    except Presupuesto.DoesNotExist:
        # Si el presupuesto no existe
        messages.error(request, "El presupuesto que intentas eliminar no existe.")
    
    return redirect('orden:detail', codigo=codigo)


def generar_presupuesto_pdf(request, presupuesto_id):
    # Obtener el presupuesto
    from orden.models import Presupuesto
    presupuesto = Presupuesto.objects.get(id=presupuesto_id)

    # Cargar el PDF existente
    template_path = "/static/orden/presupuesto.pdf"  # Cambia esto
    doc = fitz.open(template_path)
    page = doc[0]  # Primera página del PDF

    # Insertar datos en el PDF (ajustar posiciones según el diseño)
    page.insert_text((100, 150), f"Presupuesto: {presupuesto.id}", fontsize=12)
    page.insert_text((100, 170), f"Fecha: {presupuesto.created.strftime('%d/%m/%Y')}", fontsize=12)
    page.insert_text((100, 190), f"Localidad: {presupuesto.localidad}", fontsize=12)
    page.insert_text((100, 210), f"Responsable: {presupuesto.responsable}", fontsize=12)
    page.insert_text((100, 230), f"Pago: {presupuesto.pago}", fontsize=12)
    page.insert_text((100, 250), f"Monto: ${presupuesto.monto}", fontsize=12)

    # Guardar el PDF en memoria
    output = io.BytesIO()
    doc.save(output)
    doc.close()
    output.seek(0)

    # Devolver el PDF como respuesta HTTP
    response = HttpResponse(output, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="presupuesto_{presupuesto.id}.pdf"'
    return response

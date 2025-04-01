import datetime
import os
from fillpdf import fillpdfs
from django.core.files import File
import textwrap

def dividir_texto(texto, max_length=84):
    """Divide el texto en líneas de máximo `max_length` caracteres, cortando con un guion si es necesario."""
    lineas = textwrap.wrap(texto, width=max_length, break_long_words=True)
    return [linea + "-" if i < len(lineas) - 1 else linea for i, linea in enumerate(lineas)]

def rellenar_pdf(orden, presupuesto):
    form_fields = list(fillpdfs.get_form_fields('static/presupuesto.pdf').keys())

    # Datos del PDF
    fecha = datetime.datetime.today().strftime("%d/%m/%Y")
    cliente = orden.cliente.nombre
    tel = orden.cliente.telefono
    marca = orden.vehiculo.marca
    modelo = orden.vehiculo.modelo
    patente = orden.vehiculo.patente
    precio = f"${int(presupuesto.monto):,}".replace(",", ".")

    # Obtener los servicios relacionados con la orden
    servicios = orden.obtener_servicios()
    textos_servicios = [servicio.servicio for servicio in servicios]

    # Generar las líneas con división automática
    lineas_pdf = []
    for servicio in textos_servicios:
        lineas_pdf.extend(dividir_texto(servicio, max_length=84))

    # Rellenar hasta 11 líneas con espacios en blanco si hay menos
    while len(lineas_pdf) < 11:
        lineas_pdf.append("")

    # Crear diccionario con los datos
    data_dict = {
        form_fields[0]: presupuesto.id,
        form_fields[1]: 1,
        form_fields[2]: fecha,
        form_fields[3]: cliente,
        form_fields[4]: "-",
        form_fields[5]: "Villa Constitución",
        form_fields[6]: tel,
        form_fields[7]: "A cargo",
        form_fields[8]: "Efectivo",
        form_fields[9]: marca,
        form_fields[10]: patente,
        form_fields[11]: modelo,
        form_fields[12]: "-",
        form_fields[26]: precio,
    }

    # Agregar cada línea de servicio al PDF
    for i in range(11):
        data_dict[form_fields[13 + i]] = lineas_pdf[i] if i < len(lineas_pdf) else ""

    # Ruta de guardado
    pdf_filename = f"{cliente}_{orden.codigo}.pdf"
    pdf_path = os.path.join("media/presupuestos", pdf_filename)

    # Llenar y guardar el PDF
    fillpdfs.write_fillable_pdf("static/presupuesto.pdf", pdf_path, data_dict)

    # Guardar en el modelo Presupuesto
    with open(pdf_path, "rb") as f:
        presupuesto.archivo_pdf.save(pdf_filename, File(f))

    return presupuesto.archivo_pdf.url

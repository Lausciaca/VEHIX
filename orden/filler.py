import datetime
import os
from fillpdf import fillpdfs
from django.core.files import File

def rellenar_pdf(orden, presupuesto):
    form_fields = list(fillpdfs.get_form_fields('static/presupuesto.pdf').keys())

    # Datos del PDF
    fecha = datetime.datetime.today().strftime("%d/%m/%Y")  # Formato dd/mm/yyyy
    cliente = orden.cliente.nombre
    tel = orden.cliente.telefono
    marca = orden.vehiculo.marca
    modelo = orden.vehiculo.modelo
    patente = orden.vehiculo.patente

    precio = f"${int(presupuesto.monto):,}".replace(",", ".")

    data_dict = {
        form_fields[0]: orden.codigo,
        form_fields[1]: 1,  # Página
        form_fields[2]: fecha,
        form_fields[3]: cliente,
        form_fields[4]: "-",  # Dirección (si no hay)
        form_fields[5]: "Villa Constitución",
        form_fields[6]: tel,
        form_fields[7]: "A cargo",
        form_fields[8]: "Efectivo",
        form_fields[9]: marca,
        form_fields[10]: patente,
        form_fields[11]: modelo,
        form_fields[12]: "-",  # Color
        form_fields[13]: "Sustitución de paragolpes delantero y guardabarros derecho",
        form_fields[14]: "Difuminado de puerta delantera derecha y guardabarros delantero izquierdo",
        form_fields[26]: precio,
    }

    # Ruta de guardado
    pdf_filename = f"{cliente}_{orden.codigo}.pdf"
    pdf_path = os.path.join("media/presupuestos", pdf_filename)

    # Llenar el PDF y guardarlo
    fillpdfs.write_fillable_pdf("static/presupuesto.pdf", pdf_path, data_dict)

    # Guardar en el modelo
    with open(pdf_path, "rb") as f:
        presupuesto.archivo_pdf.save(pdf_filename, File(f))

    return presupuesto.archivo_pdf.url

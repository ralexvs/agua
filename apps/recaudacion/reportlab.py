import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate
from reportlab.lib import colors

from .models import Recaudacion, RecaudacionDetalle
from apps.parametro.models import Entidad


def reporte(request,pk):
  w, h = A4
  x = 40
  y = h - 100
  # Obtenemos un queryset, para un determinado planilla usando pk.
  try:
    entidad = Entidad.objects.all().first()
    recaudacion = Recaudacion.objects.get(id=pk)
    detalle = RecaudacionDetalle.objects.filter(recaudacion=pk)

  except ValueError:  # Si no existe llamamos a "pagina no encontrada".
    raise Http404()

  # Creamos un objeto HttpResponse con las cabeceras del PDF correctas.

  # Cree un buffer similar a un archivo para recibir datos PDF.
  buffer = io.BytesIO()
  # Cree el objeto PDF, utilizando el búfer como su "archivo".
  p = canvas.Canvas(buffer, pagesize=A4)
 

  # Dibuja cosas en el PDF. Aquí es donde ocurre la generación de PDF.
  # Consulte la documentación de ReportLab para ver la lista completa de funciones.
  p.roundRect(0, 795, 754, 120, 20, stroke=0, fill=1)
  p.setFillColorRGB(0, 12,153)

  # La fuente y el tamaño
  p.setFont('Helvetica',12)
  p.drawString(50, 820, str(entidad.descripcion))
  p.setFont('Helvetica', 8)
  p.drawString(250, 805,'Ruc:  ' + str(entidad.ruc))
  p.setFont('Helvetica-Bold', 8)
  p.setFillColorRGB(0, 0, 0)
  p.drawString(50, 780, 'Fecha: ')
  p.drawString(50, 760, "Pago: ")
  p.drawString(50, 740, "Descuento: ")
  p.drawString(50, 720, "Abonado: ")
  p.drawString(50, 700, "Descripción: ")

  p.drawString(350, 780, 'Consumo: ')
  p.drawString(350, 770, "Total base: ")
  p.drawString(350, 760, "Total reserva: ")
  p.drawString(350, 750, "Total excedente: ")
  p.drawString(350, 740, "Total consumo máximo: ")
  p.drawString(350, 720, "Subtotal: ")
  p.drawString(350, 710, "Total descuento: ")
  p.drawString(350, 700, "Total: ")


# Obtenemos el titulo de un libro y la portada.
  p.setFont('Helvetica', 8)
  p.drawString(100, 780, str(recaudacion.fecha))
  p.drawString(100, 760, str(recaudacion.pago))
  p.drawString(110, 740,  str(recaudacion.descuento))
  p.drawString(100, 720, str(recaudacion.abonado))
  p.drawString(115, 700, recaudacion.descripcion)

  p.drawString(500, 780, str(recaudacion.total_consumo)+ ' M3')
  p.drawString(500, 770, str(recaudacion.total_base))
  p.drawString(500, 760, str(recaudacion.total_base_reserva))
  p.drawString(500, 750, str(recaudacion.total_excedente))
  p.drawString(500, 740, str(recaudacion.total_consumo_maximo))
  p.drawString(500, 720, str(recaudacion.subtotal))
  p.drawString(500, 710, str(recaudacion.total_descuento))
  p.setFont('Helvetica-Bold', 10)
  p.drawString(500, 700, str(recaudacion.total_general))

  p.line(40, h-150, 550, h-150)

  i = 10
  p.setFont('Helvetica-Bold', 8)
  p.drawString(80, 680-i, 'Periodo')
  p.drawString(130, 680-i, 'Lec. Act')
  p.drawString(180, 680-i, 'Lec. Ant')
  p.drawString(230, 680-i, 'Consumo')
  p.drawString(280, 680-i, 'Base')
  p.drawString(330, 680-i, 'Reserva')
  p.drawString(380, 680-i, 'Cons.máx.')
  p.drawString(430, 680-i, 'Excedente')
  p.drawString(480, 680-i, 'Total')
  p.setFont('Helvetica', 8)
  for dt in detalle:
    p.drawString(80, 660-i, str(dt.lectura.lectura))
    p.drawString(130, 660-i, str(dt.lectura_anterior))
    p.drawString(180, 660-i, str(dt.lectura_actual))
    p.drawString(230, 660-i, str(dt.consumo))
    p.drawString(280, 660-i, str(dt.base))
    p.drawString(330, 660-i, str(dt.base_reserva))
    p.drawString(380, 660-i, str(dt.valor_consumo_maximo))
    p.drawString(430, 660-i, str(dt.valor_excedente))
    p.drawString(480, 660-i, str(dt.total))

    i= i+10
  # Cierre el objeto PDF limpiamente y listo.
  p.showPage()
  p.save()
  # FileResponse establece el encabezado Content-Disposition para que los navegadores
  # presenta la opción para guardar el archivo.
  buffer.seek(0)

  return FileResponse(buffer, as_attachment=False, filename='hello.pdf')

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate
from reportlab.lib import colors
import datetime
from django.utils import timezone
from .models import Recaudacion, RecaudacionDetalle
from apps.parametro.models import Entidad


def planilla_recaudada(request,pk):
  ahora = timezone.now().strftime("%d/%b/%Y %Z %H:%M:%S")
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
  #p.roundRect(0, 795, 754, 120, 20, stroke=0, fill=1)
  #p.setFillColorRGB(0, 12,153)

  # La fuente y el tamaño
  p.setFont('Courier', 10)
  p.drawString(50, 810, str(entidad.descripcion))
  p.setFont('Courier', 7)
  p.drawString(420, 820, str(ahora))
  
  p.drawString(510, 820, request.user.username)
  p.setLineWidth(0.5)
  p.line(415,815, 560,815)
  p.setFont('Courier-Bold', 8)
  
  p.drawString(50, 780, 'Fecha: ')
  p.drawString(160, 780, "Descuentos.:")
  p.drawString(50, 760, "Pago: ")
  p.drawString(180, 760, "Teléfono: ")
  p.drawString(50, 740, "Identificación: ")
  p.drawString(230, 740, 'Consumo:      m3')
  p.drawString(50, 720, "Abonado:")
  p.drawString(50, 700, "Descripción: ")
  
  p.drawString(350, 780, "Agua Potable: ")
  p.drawString(350, 770, "Derecho conexion: ")
  p.drawString(350, 760, "Alcantarillado: ")
  p.drawString(350, 750, "Administracion: ")
  p.drawString(350, 740, "Otros valores: ")
  p.drawString(350, 720, "Subtotal: ")
  p.drawString(350, 710, "Total descuento: ")
  p.drawString(350, 700, "Total: ")


# Obtenemos el titulo de un libro y la portada.
  p.setFont('Courier', 8)
  p.drawString(100, 780, str(recaudacion.fecha))
  p.drawString(220, 780,  str(recaudacion.descuento))
  p.drawString(100, 760, str(recaudacion.pago))
  
  if str(recaudacion.abonado.telefono)!='None':
    p.drawString(240, 760, str(recaudacion.abonado.telefono))
  elif str(recaudacion.abonado.celular) != 'None':
    p.drawString(240, 760, str(recaudacion.abonado.celular))
  
  p.drawString(130, 740, str(recaudacion.abonado.identificacion))
  p.drawString(100, 720, str(recaudacion.abonado))
  
  p.drawString(115, 700, recaudacion.descripcion)
  p.drawString(280, 740, str(recaudacion.total_consumo))
  agua = recaudacion.total_base + recaudacion.total_base_reserva + recaudacion.total_excedente+recaudacion.total_consumo_maximo
  p.drawString(500, 780, str(agua))
  p.drawString(500, 770, str(recaudacion.total_derecho_conexion))
  p.drawString(500, 760, str(recaudacion.total_alcantarillado))
  p.drawString(500, 750, str(recaudacion.total_administracion))
  p.line(485, 735, 535, 735)
  p.drawString(500, 720, str(recaudacion.subtotal))
  p.drawString(500, 710, str(recaudacion.total_descuento))
  p.setFont('Courier-Bold', 10)
  p.setFillColorRGB(253, 0, 0)
  p.drawString(498, 700, str(recaudacion.total_general))
  p.line(485, 695, 535, 695)
  p.line(485, 693, 535, 693)
  p.setFillColorRGB(0, 0, 0)
  #p.setLineWidth(1)
  p.setDash(6, 3)
  p.line(50, h-160, 550, h-160)
  p.line(50, h-180, 550, h-180)
  i = 10
  p.setFont('Courier-Bold', 7)
  p.drawString(60, 680-i, 'Periodo')
  p.drawString(108, 680-i, 'Servicio')
  p.drawString(165, 680-i, 'Medidor')
  p.drawString(275, 685-i, 'Lectura')
  p.drawString(210, 680-i, 'M. Cálculo')
  p.drawString(255, 675-i, 'Anterior')
  p.drawString(300, 675-i, 'Actual')
  p.drawString(335, 680-i, 'Consumo')
  p.drawString(370, 680-i, 'Base')
  p.drawString(395, 680-i, 'Reserva')
  p.drawString(430, 680-i, 'Cons.máx.')
  p.drawString(475, 680-i, 'Excedente')
  p.drawString(520, 680-i, 'Total')
  p.setFont('Courier', 8)
  for dt in detalle:
    bases = dt.base + dt.base_reserva
    p.drawString(55, 660-i, str(dt.lectura.lectura))
    p.drawString(100, 660-i, str(dt.lectura.catastro.servicio))
    p.drawString(160, 660-i, str(dt.lectura.catastro.medidor))
    p.drawString(210, 660-i, str(dt.lectura.tipo_lectura))
    p.drawString(260, 660-i, str(dt.lectura_anterior))
    p.drawString(300, 660-i, str(dt.lectura_actual))
    p.drawString(345, 660-i, str(dt.consumo))
    p.drawString(370, 660-i, str(dt.base))
    p.drawString(395, 660-i, str(dt.base_reserva))
    p.drawString(440, 660-i, str(dt.valor_consumo_maximo))
    p.drawString(485, 660-i, str(dt.valor_excedente))
    p.drawString(520, 660-i, str(dt.total))
    
    

    i= i+10
  # Cierre el objeto PDF limpiamente y listo.
  p.showPage()
  p.save()
  # FileResponse establece el encabezado Content-Disposition para que los navegadores
  # presenta la opción para guardar el archivo.
  buffer.seek(0)

  return FileResponse(buffer, as_attachment=False, filename='hello.pdf')

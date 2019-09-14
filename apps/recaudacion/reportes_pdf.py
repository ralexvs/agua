from io import BytesIO
from django.http import HttpResponse
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.colors import pink, black, red, blue, green

import datetime
from django.utils import timezone
from .models import Recaudacion, RecaudacionDetalle, RecaudacionMultaDetalle
from apps.parametro.models import Entidad

PAGE_WIDTH = A4[0]
PAGE_HEIGHT = A4[1]

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
    rec_mul_det = RecaudacionMultaDetalle.objects.filter(recaudacion=pk)

  except ValueError:  # Si no existe llamamos a "pagina no encontrada".
    raise Http404()

  # Creamos un objeto HttpResponse con las cabeceras del PDF correctas.

  # Cree un buffer similar a un archivo para recibir datos PDF.
  buffer = BytesIO()
  # Cree el objeto PDF, utilizando el búfer como su "archivo".
  p = canvas.Canvas(buffer, pagesize=A4)
 

  # Dibuja cosas en el PDF. Aquí es donde ocurre la generación de PDF.
  # Consulte la documentación de ReportLab para ver la lista completa de funciones.
  #p.roundRect(0, 795, 754, 120, 20, stroke=0, fill=1)
  #p.setFillColorRGB(0, 12,153)

  # La fuente y el tamaño
  p.setFont('Courier', 10)
  
  p.setFillColorRGB(0, 0, 0.77)
  p.drawString(50, 810, str(entidad.descripcion))
  p.setFillColorRGB(0, 0, 0)
  p.setFont('Courier', 7)
  p.drawString(420, 820, str(ahora))
  
  p.setStrokeColor(green)
  p.drawString(510, 820, request.user.username)
  p.setLineWidth(0.5)
  p.line(415,815, 560,815)
  p.setFont('Courier-Bold', 8)
  
  p.drawString(50, 780, 'Fecha: ')
  p.drawString(160, 780, "Descuentos.:")
  p.drawString(340, 780, "Pago: ")
  p.drawString(450, 780, "Teléfono: ")
  p.drawString(50, 770, "Identificación: ")
  p.drawString(240, 770, 'Consumo:      m3')
  p.drawString(340, 770, 'Servicio:')
  p.drawString(450, 770, 'Medidor:')
  p.drawString(50, 760, "Abonado:")
  p.drawString(240, 760, "Dirección:")

# Obtenemos el titulo de un libro y la portada.
  p.setFont('Courier', 8)
  p.drawString(100, 780, str(recaudacion.fecha))
  p.drawString(220, 780,  str(recaudacion.descuento))
  p.drawString(370, 780, str(recaudacion.pago))
  
  if str(recaudacion.abonado.telefono)!='None':
    p.drawString(495, 780, str(recaudacion.abonado.telefono))
  elif str(recaudacion.abonado.celular) != 'None':
    p.drawString(490, 780, str(recaudacion.abonado.celular))
  
  p.drawString(130, 770, str(recaudacion.abonado.identificacion))
  p.drawString(100, 760, str(recaudacion.abonado))
  p.drawString(300, 760, str(recaudacion.abonado.direccion))
  p.drawString(290, 770, str(recaudacion.total_consumo))
  
  i = 740
  #p.setFillColorRGB(0, 0, 0)
  #p.setLineWidth(1)
  p.setDash(6, 3)
  p.line(145, h-i/8.2, 550, h-i/8.2)
  p.line(145, h-i/6.7, 550, h-i/6.7)
  
  p.setFont('Courier-Bold', 7)
  p.drawString(150, i, 'Periodo')
  p.drawString(200, i, 'M. Cálculo')
  p.drawString(275, i+5, 'Lectura')
  p.drawString(255, i-5, 'Anterior')
  p.drawString(300, i-5, 'Actual')
  p.drawString(335, i, 'Consumo')
  p.drawString(370, i, 'Base')
  p.drawString(395, i, 'Reserva')
  p.drawString(430, i, 'Cons.máx.')
  p.drawString(475, i, 'Excedente')
  p.drawString(520, i, 'Total')
  p.setFont('Courier', 8)
  i = i - 10
  j = 10
  for dt in detalle:
    bases = dt.base + dt.base_reserva
    p.drawString(150, i-j, str(dt.lectura_detalle.lectura))
    servicio = str(dt.lectura_detalle.catastro.servicio)
    medidor = str(dt.lectura_detalle.catastro.medidor)
    p.drawString(210, i-j, str(dt.lectura_detalle.tipo_lectura))
    p.drawString(260, i-j, str(dt.lectura_anterior))
    p.drawString(300, i-j, str(dt.lectura_actual))
    p.drawString(345, i-j, str(dt.consumo))
    p.drawString(370, i-j, str(dt.base))
    p.drawString(395, i-j, str(dt.base_reserva))
    p.drawString(440, i-j, str(dt.valor_consumo_maximo))
    p.drawString(485, i-j, str(dt.valor_excedente))
    p.drawString(520, i-j, str(dt.total))
    i= i - 10
    l = i
  j = 10  
  i = i -15
  l= i
  p.setFont('Courier-Bold', 8)
  p.drawString(50, i, 'Multas y otros valores')
  p.drawString(190, i, 'Cant.')
  p.drawString(230, i, 'P.Unit.')
  p.drawString(270, i, 'Total')

  p.setFont('Courier', 7)
  
  for rmd in rec_mul_det:
    p.drawString(50, i-j, str(rmd.multa.descripcion))
    p.drawString(200, i-j, str(rmd.cantidad))
    p.drawString(235, i-j, str(rmd.valor))
    p.setStrokeColor(green)
    p.drawString(270, i-j, str(rmd.total))
    i = i - 10
  p.setDash(0, 0)
  p.line(260, i-2, 300, i-2)
  p.setFont('Courier-Bold',7)
  p.drawString(270, i-j, str(recaudacion.total_otros))
  

  p.drawString(50, i-j-5, "Descripción: ")
  p.drawString(50, i-j-15, recaudacion.descripcion)

  p.setFont('Courier', 7)
  p.drawString(390, 770, str(servicio))
  p.drawString(495, 770, str(medidor))

  p.drawString(350, l, "Agua Potable: ")
  p.drawString(350, l-10, "Derecho conexion: ")
  p.drawString(350, l-20, "Alcantarillado: ")
  p.drawString(350, l-30, "Administracion: ")
  p.drawString(350, l-40, "Multas y otros valores: ")
  p.drawString(350, l-50, "Subtotal: ")
  p.drawString(350, l-60, "Total descuento: ")
  p.drawString(350, l-70, "Total: ")

  agua = recaudacion.total_base + recaudacion.total_base_reserva + \
      recaudacion.total_excedente+recaudacion.total_consumo_maximo
  p.drawString(500, l, str(agua))
  p.drawString(500, l-10, str(recaudacion.total_derecho_conexion))
  p.drawString(500, l-20, str(recaudacion.total_alcantarillado))
  p.drawString(500, l-30, str(recaudacion.total_administracion))
  p.setStrokeColor(green)
  p.drawString(500, l-40, str(recaudacion.total_otros))
  p.line(485, l-42, 535, l-42)
  p.drawString(500, l-50, str(recaudacion.subtotal))
  p.drawString(500, l-60, str(recaudacion.total_descuento))
  p.setFont('Courier-Bold', 10)
  #p.setFillColorRGB(0,0,0.77)
  p.drawString(498, l-70, str(recaudacion.total_general))

  p.line(485, l-75, 535, l-75)
  p.line(485, l-80, 535, l-80)


  # Cierre el objeto PDF limpiamente y listo.
  p.showPage()
  p.save()
  # FileResponse establece el encabezado Content-Disposition para que los navegadores
  # presenta la opción para guardar el archivo.
  buffer.seek(0)

  return FileResponse(buffer, as_attachment=False, filename='planilla.pdf')

def informe_caja_pdf(reuqest, fecha_inicial=None, fecha_final=None):
  response = HttpResponse(content_type='application/pdf')
  pdf_name='informe_caja.pdf'
  buffer = BytesIO()
  doc = SimpleDocTemplate(
    buffer,
    pagezise=A4,
    rightMargin=5,
    leftMargin=5,
    topMargin=5,
    bottomMargin=2,
  )
  elementos = []
  # Estilos
  estilo = getSampleStyleSheet()

  # Cabecera
  text = '''
          <strong ><font size=14>REPORTE</font></strong>
      '''
  header = Paragraph('REPORTE DE PLANILLAS RECAUDADAS', estilo["Title"])
  elementos.append(header)
  headings = ('Fecha', 'Nombre', 'Pago', 'Subtotal', 'Desc.', 'Total')
  allplanillas = [(p.fecha, p.abonado, p.pago, p.subtotal, p.total_descuento, p.total_general)
                  for p in Recaudacion.objects.all()]

  t = Table([headings] + allplanillas, colWidths=(65, 190, 100, 50, 50, 65))
  t.setStyle(TableStyle(
    [
      ('GRID', (0, 0), (5, -1), 1, colors.dodgerblue),
      ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
      ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
    ]
  ))
  elementos.append(t)
  doc.build(elementos)
  response.write(buffer.getvalue())
  buffer.close()
  return response
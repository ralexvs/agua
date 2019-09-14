
from io import BytesIO 
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import Table, Paragraph
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from django.views.generic import View
from django.utils import timezone
import datetime

from .models import Recaudacion, RecaudacionDetalle
from django.conf import settings

"""
Hay dos maneras de hacer reportes usando reportlab:
“Pintando” con canvas usando coordenadas (X,Y)
Usando PLATYPUS
PLATYPUS es una libreria de alto nivel que nos permite hacer documentos complejos con mínimo esfuerzo.

De la linea:
2 Importo BytesIO nos permite un lugar de almacenamiento temporal del pdf
6 a la 10 importo todo lo que necesitare para generar mi documento:
SimpleDocTemplate: La plantilla del documento
Paragraph: Para escribir párrafos
TableSytle: Lo que hará bonita a nuestra tabla
getSampleStyleSheet: Importamos una clase de hoja de estilo
colors: Esto aún no descubro que hace 😆
letter: El tamaño de la hoja
Table: Nos permite crear tablas (igual esta el longTable)
23 decimos que va a hacer un documento PDF
24 damos el nombre al documento
26 descomentamos la linea si queremos descargar el documento a nuestra computadora
27 almacenamos BytesIO a la variable buff
28 configuramos nuestro documento
35 creamos una lista
36 almacenamos getSampleStyleSheet a una variable llamada styles
37, 38 agregamos un titulo a nuestro documento usando Paragraph
39 agregamos los encabezaos de las Columnas
40 aqui creamos una variable que almacena todos los datos que tengo en el modelo Clientes
43 creo una variable donde agrego a Table los nombres de las columnas con sus datos correspondientes que están el allclientes
44 doy color a la tabla
51 agrego todo a mi lista
52 genero el documento a partir de la lista clientes
53 Recupero el archivo almacenado
54 Librero la memoria
55 regreso la respuesta 
"""
def panilla_cobrada_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "planilla_cobrada.pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=A4,
                            rightMargin=10,
                            leftMargin=30,
                            topMargin=40,
                            bottomMargin=20,
                            )
    elementos = []
    # Estilos
    styles = getSampleStyleSheet()

    # Cabecera
    text = '''
        <strong ><font size=14>REPORTE</font></strong>
    '''
    header = Paragraph('REPORTE DE PLANILLAS RECAUDADAS', styles["Title"])
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
    response.write(buff.getvalue())
    buffer.close()
    return response

class ReportePlanillaPDF(View):
  
    def cabecera(self,pdf):
        #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen = settings.MEDIA_ROOT+'/parametro/logo.jpg'
        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen, 15, 800, 120, 30,preserveAspectRatio=True)
        
        #Header
        #
        pdf.setLineWidth(.3)
        #Establecemos el tamaño de letra en 22 y el tipo de letra Helvetica
        pdf.setFont("Helvetica", 22)
        #Dibujamos una cadena en la ubicación X,Y especificada
        pdf.drawString(130, 810, u"Asoftel")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(130, 790, u"REPORTE DE PLANILLAS COBRADAS")
        pdf.setFont("Helvetica", 8)
        pdf.drawString(420, 810, datetime.datetime.isoformat(timezone.now()))
        pdf.line(410,805,560,805)
    
    def tabla(self, pdf, y):
        #Creamos una tupla de encabezados para neustra tabla
        encabezados = ('No.','Fecha', 'Nombre', 'Pago', 'Subtotal', 'Desc.', 'Total')
        #Creamos una lista de tuplas que van a contener a las personas
        detalles = [(p.id,p.fecha, p.abonado, p.pago, p.subtotal, p.total_descuento, p.total_general)
                    for p in Recaudacion.objects.all()]
        #Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_orden = Table([encabezados] + detalles,
                              colWidths=(25, 55, 185, 100, 50, 50, 65))
        #Aplicamos estilos a las celdas de la tabla
        detalle_orden.setStyle(TableStyle(
        [
            #La primera fila(encabezados) va a estar centrada
            ('ALIGN', (0, 0), (3, 0), 'CENTER'),
            #Los bordes de todas las celdas serán de color azul y con un grosor de 1
            ('GRID', (0, 0), (6, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
            #El tamaño de las letras de cada una de las celdas será de 10
            ('FONTSIZE', (0, 0), (-1, -1), 9),
        ]
        ))
       
        #Establecemos el tamaño de la hoja que ocupará la tabla
        detalle_orden.wrapOn(pdf, 800, 600)
        #Definimos la coordenada donde se dibujará la tabla
        detalle_orden.drawOn(pdf, 40, y)


    def get(self, request, *args, **kwargs):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')
        # Si deseas descargar el pdf a tu computadora
        pdf_name = "planilla_cobrada.pdf"
        #response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()
        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer, pagesize=A4)
        #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(pdf)
        y = 680
        self.tabla(pdf, y)

        #Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue() # Obtnenemos el valor del buffer
        buffer.close() #Cerramos el buffer
        response.write(pdf) #Escribimos el buffer en el response
        return response


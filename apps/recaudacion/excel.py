import csv
from django.http import HttpResponse
from .models import Recaudacion


def planilla_cobrada_csv(request):
  # Crear el objeto HttpResponse con sus cabeceras
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename="planilla_cobrada.csv"'

  # Se usa el response como un "archivo" destino
  writer = csv.writer(response)

  # Obtener los objetos que deseas exportar e iterar
  objetos = Recaudacion.objects.all()
  writer.writerow(['Fecha', 'Abonado', 'Subtotal', 'Descuento','Total'])
  for objeto in objetos:
    row = [
        objeto.fecha,
        objeto.abonado,
        objeto.subtotal,
        objeto.total_descuento,
        objeto.total_general
    ]
    writer.writerow(row)
  return response

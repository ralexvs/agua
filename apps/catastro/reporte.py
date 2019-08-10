import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Lectura, LecturaDetalle
from django.utils import timezone

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path

def reporte_lecturas(request):
    template_path = 'catastro/reportes/lectura_print_all.html'
    today = timezone.now()

    lecturas = Lectura.objects.all()
    context={
        'obj':lecturas,
        'today':today,
        'request': request
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline'; filename='todas_las_lecturas'
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisaStatus.err:
       return HttpResponse('Tuvimos algunos errores <pre>' + html + '</pre>')
    return response


def reporte_lectura(request, lectura_id):
    template_path = 'catastro/reportes/lectura_print_one.html'
    today = timezone.now()

    enc = Lectura.objects.filter(id=lectura_id).first()
    if enc:
        detalle = LecturaDetalle.objects.filter(lectura__id=lectura_id)
    else:
        detalle={}
    
    context = {
        'detalle':detalle,
        'encabezado':enc,
        'today': today,
        'request':request
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline'
    filename = 'Lectura'
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisaStatus = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisaStatus.err:
           return HttpResponse('Tuvimos algunos errores <pre>' + html + '</pre>')
    return response

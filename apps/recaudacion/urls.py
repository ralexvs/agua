from django.urls import path
from .views import LecturaDetalleList, RecaudacionList, recaudacion, RecaudacionCreate
from .reporte import reporte_deudores
urlpatterns = [
    path('recaudaciones/', LecturaDetalleList.as_view(),
         name='lectura_detalle_list'),
    path('recaudaciones/list', RecaudacionList.as_view(), name='recaudacion_list'),
    path('recaudaciones/create/<int:catastro_id>',
         recaudacion, name='recaudacion_create'),
    path('recaudaciones/update/<int:recaudacion_id>/', recaudacion, name='recaudacion_update'),
     
    path('recaudaciones/new/', RecaudacionCreate.as_view(), name='recaudacion_create_r'),

    path('recaudaciones/reportes/deudores', reporte_deudores, name='reporte_deudores'),

]

     

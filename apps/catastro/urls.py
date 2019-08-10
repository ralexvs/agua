from django.urls import path
from .views import (
    MedidorList, MedidorCreate, MedidorUpdate, MedidorDelete, medidor_inactivar,
    BarrioList, BarrioCreate, BarrioUpdate, BarrioDelete, barrio_inactivar,
    AbonadoList, AbonadoCreate, AbonadoUpdate, AbonadoDelete, abonado_inactivar, abonado_inactivar_js, search,
    CatastroList, CatastroCreate, CatastroUpdate, CatastroDelete, catastro_inactivar, catastro_suspender_servicio,
    TipoLecturaList, TipoLecturaCreate, TipoLecturaUpdate, TipoLecturaDelete, tipolectura_inactivar,
    LecturaList,  LecturaDelete, lectura_inactivar, lectura, 
    LecturaDetalleDelete, 
)
from .reporte import reporte_lecturas, reporte_lectura

urlpatterns = [
     path('medidores/', MedidorList.as_view(), name='medidor_list'),
     path('medidores/create/', MedidorCreate.as_view(), name='medidor_create'),
     path('medidores/update/<int:pk>',
          MedidorUpdate.as_view(), name='medidor_update'),
     path('medidores/delete/<int:pk>',
          MedidorDelete.as_view(), name='medidor_delete'),
     path('medidores/inactivar/<int:id>',
          medidor_inactivar, name='medidor_inactivar'),

     path('barrios/', BarrioList.as_view(), name='barrio_list'),
     path('barrios/create/', BarrioCreate.as_view(), name='barrio_create'),
     path('barrios/update/<int:pk>', BarrioUpdate.as_view(), name='barrio_update'),
     path('barrios/delete/<int:pk>', BarrioDelete.as_view(), name='barrio_delete'),
     path('barrios/inactivar/<int:id>', barrio_inactivar, name='barrio_inactivar'),

     path('abonados/', AbonadoList.as_view(), name='abonado_list'),
     path('abonados/create/', AbonadoCreate.as_view(), name='abonado_create'),
     path('abonados/update/<int:pk>',
          AbonadoUpdate.as_view(), name='abonado_update'),
     path('abonados/delete/<int:pk>',
          AbonadoDelete.as_view(), name='abonado_delete'),
     path('abonados/inactivar/<int:id>',
          abonado_inactivar, name='abonado_inactivar'),
     path('abonados/estado/<int:id>',
          abonado_inactivar_js, name='abonado_inactivar_js'),
    path('abonados/buscar/', search, name='buscar'),

     path('catastros/', CatastroList.as_view(), name='catastro_list'),
     path('catastros/create/', CatastroCreate.as_view(), name='catastro_create'),
     path('catastros/update/<int:pk>', CatastroUpdate.as_view(), name='catastro_update'),
     path('catastros/delete/<int:pk>', CatastroDelete.as_view(), name='catastro_delete'),
     path('catastros/inactivar/<int:id>', catastro_inactivar, name='catastro_inactivar'),
     path('catastros/suspender/<int:id>',
          catastro_suspender_servicio, name='catastro_suspender_servicio'),

     path('tipolecturas/', TipoLecturaList.as_view(), name='tipolectura_list'),
     path('tipolecturas/create', TipoLecturaCreate.as_view(), name='tipolectura_create'),
     path('tipolecturas/update/<int:pk>', TipoLecturaUpdate.as_view(), name='tipolectura_update'),
     path('tipolecturas/delete/<int:pk>', TipoLecturaDelete.as_view(), name='tipolectura_delete'),
     path('tipolecturas/inactivar/<int:id>', tipolectura_inactivar, name='tipolectura_inactivar'),

     path('lecturas/', LecturaList.as_view(), name='lectura_list'),
     path('lecturas/create', lectura, name='lectura_create'),
     path('lecturas/update/<int:lectura_id>', lectura, name='lectura_update'),
     path('lecturas/delete/<int:pk>', LecturaDelete.as_view(), name='lectura_delete'),
     path('lecturas/inactivar/<int:id>', lectura_inactivar, name='lectura_inactivar'),
     
     path('lecturas/<int:lectura_id>/delete/<int:pk>/',LecturaDetalleDelete.as_view(), name='lecturadetalle_delete'),
     
     path('lecturas/print_all', reporte_lecturas, name='lectura_print_all'),
     path('lecturas/<int:lectura_id>/imprimir', reporte_lectura, name='lectura_print_one'),

]

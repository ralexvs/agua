from django.urls import path
from .views import (
    EntidadList, EntidadCreate, EntidadUpdate, EntidadDelete, entidad_inactivar,
    ServicioList, ServicioCreate, ServicioUpdate, ServicioDelete, servicio_inactivar,
    TarifaList, TarifaCreate, TarifaUpdate, TarifaDelete, tarifa_inactivar,
    MultaList, MultaCreate, MultaUpdate, MultaDelete, multa_inactivar,
    DescuentoList, DescuentoCreate, DescuentoUpdate, DescuentoDelete, descuento_inactivar,
    PagoList, PagoCreate, PagoUpdate, PagoDelete, pago_inactivar,
    )

urlpatterns = [
    path('entidades/', EntidadList.as_view(), name='entidad_list'),
    path('entidades/create/', EntidadCreate.as_view(), name='entidad_create'),
    path('entidades/update/<int:pk>', EntidadUpdate.as_view(), name='entidad_update'),
    path('entidades/delete/<int:pk>', EntidadDelete.as_view(), name='entidad_delete'),
    path('entidades/inactivar/<int:id>',entidad_inactivar, name='entidad_inactivar'),

    path('servicios/', ServicioList.as_view(), name='servicio_list'),
    path('servicios/create/', ServicioCreate.as_view(), name='servicio_create'),
    path('servicios/update/<int:pk>', ServicioUpdate.as_view(), name='servicio_update'),
    path('servicios/delete/<int:pk>', ServicioDelete.as_view(), name='servicio_delete'),
    path('servicios/inactivar/<int:id>', servicio_inactivar, name='servicio_inactivar'),

    path('tarifas/', TarifaList.as_view(), name='tarifa_list'),
    path('tarifas/create/', TarifaCreate.as_view(), name='tarifa_create'),
    path('tarifas/update/<int:pk>', TarifaUpdate.as_view(), name='tarifa_update'),
    path('tarifas/delete/<int:pk>', TarifaDelete.as_view(), name='tarifa_delete'),
    path('tarifas/inactivar/<int:id>', tarifa_inactivar, name='tarifa_inactivar'),

    path('multas/', MultaList.as_view(), name='multa_list'),
    path('multas/create/', MultaCreate.as_view(), name='multa_create'),
    path('multas/update/<int:pk>', MultaUpdate.as_view(), name='multa_update'),
    path('multas/delete/<int:pk>', MultaDelete.as_view(), name='multa_delete'),
    path('multas/inactivar/<int:id>', multa_inactivar, name='multa_inactivar'),

    path('descuentos/', DescuentoList.as_view(), name='descuento_list'),
    path('descuentos/create/', DescuentoCreate.as_view(), name='descuento_create'),
    path('descuentos/update/<int:pk>',
         DescuentoUpdate.as_view(), name='descuento_update'),
    path('descuentos/delete/<int:pk>',
         DescuentoDelete.as_view(), name='descuento_delete'),
    path('descuentos/inactivar/<int:id>',
         descuento_inactivar, name='descuento_inactivar'),

    path('pagos/', PagoList.as_view(), name='pago_list'),
    path('pagos/create/', PagoCreate.as_view(), name='pago_create'),
    path('pagos/update/<int:pk>', PagoUpdate.as_view(), name='pago_update'),
    path('pagos/delete/<int:pk>', PagoDelete.as_view(), name='pago_delete'),
    path('pagos/inactivar/<int:id>', pago_inactivar, name='pago_inactivar'),
]

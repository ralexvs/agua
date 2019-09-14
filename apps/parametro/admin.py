from django.contrib import admin
from .models import Entidad, Pago, Servicio, Tarifa, Multa, Descuento
from import_export.admin import ImportExportModelAdmin

# Register your models here.

@admin.register(Entidad, Pago, Servicio, Tarifa, Multa, Descuento)
class ViewAdmin(ImportExportModelAdmin):
    pass

# Register your models here.

from django.contrib import admin
from .models import Recaudacion, RecaudacionDetalle
from import_export.admin import ImportExportModelAdmin

# Register your models here.

@admin.register(Recaudacion, RecaudacionDetalle)
class ViewAdmin(ImportExportModelAdmin):
    pass
# Register your models here.

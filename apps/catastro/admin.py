from django.contrib import admin
from .models import Barrio, Catastro, Abonado, Medidor
from import_export.admin import ImportExportModelAdmin

# Register your models here.

@admin.register(Barrio, Catastro, Abonado,Medidor,)
class ViewAdmin(ImportExportModelAdmin):
    pass

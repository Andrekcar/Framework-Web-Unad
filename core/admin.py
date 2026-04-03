from django.contrib import admin

# Register your models here.

from .models import Emprendedor

@admin.register(Emprendedor)
class EmprendedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_documento', 'documento', 'actividad_economica', 'sector', 'telefono', 'email', 'direccion')
    editable_fields = ('nombre', 'tipo_documento', 'documento', 'actividad_economica', 'sector', 'telefono', 'email', 'direccion')
    search_fields = ('nombre', 'documento')
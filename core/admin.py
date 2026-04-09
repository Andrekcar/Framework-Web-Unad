from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Emprendedor

# Register your models here.

from .models import Emprendedor

@admin.register(Emprendedor)
class EmprendedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_documento', 'documento', 'actividad', 'sector', 'acciones')
    search_fields = ('nombre', 'documento')

    fieldsets = (
        (None, {
            'fields': (
                ('nombre', 'tipo_documento', 'documento'),
                ('actividad', 'sector'),
                ('telefono', 'email'),
                'direccion',    
            )
        }),
    )

    def acciones(self, obj):
        editar = reverse('admin:core_emprendedor_change', args=[obj.pk])
        eliminar = reverse('admin:core_emprendedor_delete', args=[obj.pk])
        return format_html(
            '<div>'
            '<a href="{}" title="Ver detalles">?</a>'
            '<a href="{}" title="Editar">0</a>'
            '<a href="{}" title="Eliminar">X</a>'
            '</div>',
            editar, editar, eliminar
        )

admin.site.enable_nav_sidebar = False

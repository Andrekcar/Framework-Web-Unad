from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Emprendedor

@admin.register(Emprendedor)
class EmprendedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'actividad', 'sector', 'acciones')
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
        edit = reverse('admin:core_emprendedor_change', args=[obj.pk])
        delete = reverse('admin:core_emprendedor_delete', args=[obj.pk])
        return format_html(
            '<div>'
            '<a href="{}" title="Ver detalles">?</a>'
            '<a href="{}" title="Editar">&#9998;</a>'
            '<a href="{}" title="Eliminar">&#10005;</a>'
            '</div>',
            edit, edit, delete
        )

admin.site.enable_nav_sidebar = False
   
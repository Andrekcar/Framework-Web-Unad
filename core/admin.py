from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Emprendedor, Programas

@admin.register(Programas)
class ProgramasAdmin(admin.ModelAdmin):
    # Plantilla personalizada para administrar programas de capacitación.
    change_list_template = 'admin/core/programas/form.html'
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin', 'cupos')

@admin.register(Emprendedor)
class EmprendedorAdmin(admin.ModelAdmin):
    # Configuración de la vista de administrador para emprendedores.
    # Aquí se define qué columnas se muestran y qué campos se pueden buscar.
    list_display = ('nombre', 'actividad', 'sector', 'acciones')
    search_fields = ('nombre', 'documento')

    fieldsets = (
        (None, {
            # Campos agrupados para facilitar la edición/registro de datos del emprendedor.
            'fields': (
                ('nombre', 'tipo_documento', 'documento'),
                ('actividad', 'sector'),
                ('telefono', 'email'),
                'direccion',
            )
        }),
    )

    def acciones(self, obj):
        # Enlaces rápidos en la lista de emprendedores: editar y eliminar.
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
   
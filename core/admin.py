from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Emprendedor, Programas, observaciones

@admin.register(Programas)
class ProgramasAdmin(admin.ModelAdmin):
    change_list_template = 'admin/core/programas/form.html'
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin', 'cupos')


@admin.register(Emprendedor)
class EmprendedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'actividad', 'sector', 'programa', 'acciones')
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

@admin.register(observaciones)
class ObservacionesAdmin(admin.ModelAdmin):
    change_list_template = 'admin/core/emprendedor/change_obs_form.html'
    list_display = ('emprendedor', 'programa', 'fecha', 'observacion')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.enable_nav_sidebar = False
   
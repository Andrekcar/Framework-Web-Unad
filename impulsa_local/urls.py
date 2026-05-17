"""
URL configuration for impulsa_local project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from core.forms import EmprendedorPasswordResetForm
from core.views import home, emp_home, inscribir, guardar_observacion, editar_emprendedor, programas_list, reportes

urlpatterns = [
    # Ruta para el módulo de reportes (solo staff) — debe ir antes de admin.site.urls
    path("admin/reportes/", reportes, name="reportes"),

    # /admin/ exacto → redirige directo al gestor de emprendedores
    path('admin/', RedirectView.as_view(pattern_name='admin:core_emprendedor_changelist')),
    # Resto de URLs del panel de administración
    path('admin/', admin.site.urls),
    
    # formulario para ingresar el correo y reestablecer la contraseña
    path(
        "accounts/password_reset/",
        auth_views.PasswordResetView.as_view(form_class=EmprendedorPasswordResetForm),
        name="password_reset",
    ),
    
    # Incluye todas las URLs de autenticación estándar de Django (login, logout, password_change, etc.)
    path("accounts/", include("django.contrib.auth.urls")),
    
    # Página de inicio principal del sitio
    path("", home, name="home"),
    
    # Página de inicio exclusiva para emprendedores
    path("emprendedor/", emp_home, name="emp_home"),
    
    # Ruta para inscribir a un emprendedor en un programa específico (requiere ID del programa)
    path("inscribir/<int:programa_id>/", inscribir, name="inscribir"),
    
    # Ruta para guardar observaciones relacionadas con emprendedores
    path("emprendedor/observacion/", guardar_observacion, name="guardar_observacion"),
    
    # Ruta para editar la información de un emprendedor
    path("emprendedor/editar/", editar_emprendedor, name="editar_emprendedor"),

    # Ruta para listar programas disponibles
    path("emprendedor/programas/", programas_list, name="programas_list"),
]

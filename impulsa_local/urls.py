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
from core.forms import EmprendedorPasswordResetForm
from core.views import home, emp_home, inscribir, guardar_observacion, editar_emprendedor

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        "accounts/password_reset/",
        auth_views.PasswordResetView.as_view(form_class=EmprendedorPasswordResetForm),
        name="password_reset",
    ),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", home, name="home"),
    path("emprendedor/", emp_home, name="emp_home"),
    path("inscribir/<int:programa_id>/", inscribir, name="inscribir"),
    path("emprendedor/observacion/", guardar_observacion, name="guardar_observacion"),
    path("emprendedor/editar/", editar_emprendedor, name="editar_emprendedor"),
]
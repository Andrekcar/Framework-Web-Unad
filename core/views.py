from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import timezone
from core.models import Programas, Emprendedor
from core.forms import ObservacionForm, EmprendedorForm

def _es_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

def home(request):
    if _es_admin(request.user):
        logout(request)
    if request.user.is_authenticated:
        return redirect('programas_list')
    return redirect('login')

@login_required
def emp_home(request):
    if _es_admin(request.user):
        logout(request)
        return redirect('login')
    emprendedor = get_object_or_404(Emprendedor, email=request.user.email)
    return render(request, 'emprendedor/emp_home.html', {
        'emprendedor': emprendedor,
        'observacion_form': ObservacionForm(),
        'emprendedor_form': EmprendedorForm(instance=emprendedor),
    })


@login_required
def guardar_observacion(request):
    if _es_admin(request.user) or request.method != 'POST':
        return redirect('emp_home')
    emprendedor = get_object_or_404(Emprendedor, email=request.user.email)
    if emprendedor.programa:
        form = ObservacionForm(request.POST)
        if form.is_valid():
            obs = form.save(commit=False)
            obs.emprendedor = emprendedor
            obs.programa = emprendedor.programa
            obs.save()
    return redirect('emp_home')

@login_required
def editar_emprendedor(request):
    if _es_admin(request.user):
        logout(request)
        return redirect('login')
    emprendedor = get_object_or_404(Emprendedor, email=request.user.email)
    if request.method == 'POST':
        form = EmprendedorForm(request.POST, instance=emprendedor)
        if form.is_valid():
            form.save()
            return redirect('editar_emprendedor')
    else:
        form = EmprendedorForm(instance=emprendedor)
    return render(request, 'emprendedor/editar.html', {'form': form, 'emprendedor': emprendedor})

@login_required
def programas_list(request):
    if _es_admin(request.user):
        logout(request)
        return redirect('login')
    emprendedor = get_object_or_404(Emprendedor, email=request.user.email)
    hoy = timezone.now().date()
    programas = Programas.objects.filter(fecha_fin__gte=hoy)
    return render(request, 'emprendedor/programas.html', {
        'programas': programas,
        'emprendedor_programa_id': emprendedor.programa_id,
        'tiene_programa': emprendedor.programa is not None,
    })

@login_required
def inscribir(request, programa_id):
    if _es_admin(request.user):
        logout(request)
        return redirect('login')
    emprendedor = get_object_or_404(Emprendedor, email=request.user.email)
    if emprendedor.programa is not None:
        return redirect('programas_list')
    hoy = timezone.now().date()
    programa = get_object_or_404(Programas, id=programa_id, fecha_fin__gte=hoy, cupos__gt=0)
    emprendedor.programa = programa
    emprendedor.save()
    programa.cupos -= 1
    programa.save()
    return redirect('emp_home')

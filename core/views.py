from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from core.models import Programas, Emprendedor
from core.forms import ObservacionForm, EmprendedorForm

def _es_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

def home(request):
    if _es_admin(request.user):
        logout(request)
        return redirect('login')
    programs = Programas.objects.all()
    return render(request, 'home.html', {'programs': programs})

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
    if _es_admin(request.user) or request.method != 'POST':
        return redirect('emp_home')
    emprendedor = get_object_or_404(Emprendedor, email=request.user.email)
    form = EmprendedorForm(request.POST, instance=emprendedor)
    if form.is_valid():
        form.save()
    return redirect('emp_home')

@login_required
def inscribir(request, programa_id):
    if _es_admin(request.user):
        logout(request)
        return redirect('login')
    programa = get_object_or_404(Programas, id=programa_id)
    emprendedor = get_object_or_404(Emprendedor, email=request.user.email)
    if programa.cupos > 0:
        emprendedor.programa = programa
        emprendedor.save()
        programa.cupos -= 1
        programa.save()
    return redirect('emp_home')

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import admin
from django.utils import timezone
from core.models import Programas, Emprendedor
from core.forms import ObservacionForm, EmprendedorForm
import pandas as pd # Pandas
import matplotlib # Matplotlib para gráficos

matplotlib.use('Agg') #
import matplotlib.pyplot as plt # Matplotlib para gráficos
import base64 # Para codificar imágenes en base64 y mostrarlas en HTML
from io import BytesIO # Para manejar imágenes en memoria sin guardarlas en disco
from datetime import timedelta # Para calcular fechas 

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
def reportes(request):

    # ── Datos base ────────────────────────────────────────────────
    seis_meses_atras = timezone.now() - timedelta(days=180)
    emprendedores = Emprendedor.objects.all().values('sector', 'updated_at', 'programa')
    df = pd.DataFrame(emprendedores)

    # ── Reporte 1: Activos vs Inactivos ───────────────────────────
    reporte1_activos = 0
    reporte1_inactivos = 0
    img_barras = None
    if not df.empty:
        df['updated_at'] = pd.to_datetime(df['updated_at'])
        mask_activos = df['updated_at'] >= seis_meses_atras
        reporte1_activos = int(mask_activos.sum())
        reporte1_inactivos = int((~mask_activos).sum())

        fig, ax = plt.subplots(figsize=(5, 4))
        df_status = pd.DataFrame({'Estado': ['Activos', 'Inactivos'], 'Total': [reporte1_activos, reporte1_inactivos]})
        df_status.plot(kind='bar', x='Estado', y='Total', ax=ax, color=['#2ecc71', '#e74c3c'])
        ax.set_title('Emprendedores Activos vs Inactivos')
        ax.set_xlabel('Estado')
        ax.set_ylabel('Cantidad')
        ax.tick_params(axis='x', rotation=0)
        buf = BytesIO() # Guardar la figura en un buffer de memoria en formato PNG
        fig.savefig(buf, format='png', bbox_inches='tight') 
        img_barras = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close(fig) # Cerrar la figura para liberar memoria

    # ── Reporte 2: Emprendedores por Sector ───────────────────────
    reporte2_data = []
    img_pastel = None
    if not df.empty:
        sectores = df['sector'].value_counts() 
        fig, ax = plt.subplots(figsize=(5, 4))
        sectores.plot(kind='pie', ax=ax, autopct='%1.1f%%')
        ax.set_title('Emprendedores por Sector Económico')
        ax.set_ylabel('') # ocultar etiqueta del eje y
        buf = BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        img_pastel = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close(fig)

    # ── Reporte 3: Programas Más Solicitados ──────────────────────
    programas = Programas.objects.all().values('id', 'nombre')
    df_programas = pd.DataFrame(programas)
    img_barras_h = None
    
    if not df.empty and not df_programas.empty:
        conteo = df['programa'].dropna().astype(int).value_counts() 
        df_programas['inscritos'] = df_programas['id'].map(conteo).fillna(0).astype(int)
        df_programas = df_programas.sort_values('inscritos', ascending=True)

        fig, ax = plt.subplots(figsize=(5, 4))
        ax.barh(df_programas['nombre'], df_programas['inscritos'], color='#4a90d9')
        ax.set_title('Programas Más Solicitados')
        ax.set_xlabel('Inscritos')
        ax.set_ylabel('')
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True)) # indices enteros
        buf = BytesIO() 
        fig.savefig(buf, format='png', bbox_inches='tight')
        img_barras_h = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close(fig)

    # ── Contexto y respuesta ──────────────────────────────────────
    context = admin.site.each_context(request)
    context.update({
        'reporte1_activos': reporte1_activos,
        'reporte1_inactivos': reporte1_inactivos,
        'reporte2_data': reporte2_data,
        'img_barras': img_barras,
        'img_pastel': img_pastel,
        'img_barras_h': img_barras_h,
    })
    return render(request, 'admin/reportes/reportes.html', context)

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

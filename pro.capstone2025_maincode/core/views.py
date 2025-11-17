from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction, IntegrityError 
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistroForm, LoginForm, PropiedadForm, PropiedadEditForm
from .models import SpUsuario, Propiedad

# Create your views here.

def index(request):
    return render(request, "core/index.html")

def registro_view(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    nuevo_usuario = form.save(commit=False)
                    nuevo_usuario.is_active = 'Y'
                    # aquí podríamos hashear la contraseña más adelante
                    nuevo_usuario.save()
                messages.success(request, "Cuenta creada correctamente. Ahora puedes iniciar sesión.")
                return redirect('core:login')
            except IntegrityError:
                # puede fallar por rut o email duplicado según la BD
                form.add_error(None, "Ya existe un usuario con ese RUT o email.")
    else:
        form = RegistroForm()

    return render(request, 'core/registro.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            u = SpUsuario.objects.filter(
                rut=cd['rut'].strip(),
                email__iexact=cd['email'].strip(),
                pass_field=cd['password'],   # IMPORTANTE: nombre correcto del campo
                is_active='Y',
            ).first()

            if u:
                request.session['sp_user_id'] = int(u.usuario_id)
                request.session['sp_user_nombre'] = u.nombre
                request.session['sp_user_rol'] = u.rol
                messages.success(request, f"Bienvenido, {u.nombre}.")
                return redirect('core:main-registrado')
            else:
                form.add_error(None, 'Credenciales inválidas o cuenta inactiva.')
    else:
        form = LoginForm()

    return render(request, 'core/login.html', {'form': form})

def main_registrado(request):

    # Si alguien llega sin sesión, mándalo a login
    if not request.session.get('sp_user_id'):
        messages.info(request, "Inicia sesión para continuar.")
        return redirect('core:login')
    return render(request, 'core/main-registrado.html')

def salir(request):
    request.session.flush()
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect('core:login')


def ayuda_view(request):
    return render(request, "core/ayuda.html")

def nosotros_view(request):
    return render(request, "core/nosotros.html")

def mainregistrado_view(request):
    return render(request, "core/main-registrado.html")

def propiedades_view(request):
    return render(request, "core/propiedades.html")

def gestordocumentos_view(request):
    return render(request, "core/gestor-documentos.html")
    

def propiedad_view(request):
    return render(request, "core/propiedadcrud.html")

def createform_view(request):
    if request.method == 'POST':
        form = PropiedadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Propiedad creada exitosamente.")
            return redirect('core:misprop')
    else:
        form = PropiedadForm()
    return render(request, "core/createform.html", {'form': form})


# Nueva vista para crear propiedad y redirigir a usregistrado (sin afectar propiedadform_view)
def propiedadform_usreg_view(request):
    if request.method == 'POST':
        form = PropiedadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Propiedad creada exitosamente.")
            return redirect('core:usregistrado')
    else:
        form = PropiedadForm()
    return render(request, "core/propiedadform.html", {'form': form})


class PropiedadUpdateView(LoginRequiredMixin, UpdateView):
    model = Propiedad
    form_class = PropiedadForm
    template_name = 'core/propiedadform.html'
    success_url = reverse_lazy('core:misprop')

#@login_required
def editarform_view(request, pk=None):
    if pk:
        prop = get_object_or_404(Propiedad, pk=pk)
    else:
        prop = None

    if request.method == 'POST':
        form = PropiedadEditForm(request.POST, request.FILES, instance=prop)
        if form.is_valid():
            with transaction.atomic():
                obj = form.save(commit=False)
                obj.save()
            messages.success(request, "La proiedad se ha actualizado correctamente.")
            return redirect('core:misprop')
        else:
            messages.error(request, "Deben corregirse los errores en el formulario")
    else:
        form = PropiedadEditForm(instance=prop)
    #form = PropiedadEditForm()  # o PropiedadForm()
    return render(request, "core/editarform.html", {'form': form, 'propiedad': prop})


# Vista para editar propiedad con validación completa
class EditarPropiedadView(LoginRequiredMixin, UpdateView):
    model = Propiedad
    form_class = PropiedadEditForm
    template_name = 'core/editarform.html'
    success_url = reverse_lazy('core:misprop')

    

def misprop_view(request):
    propiedades = Propiedad.objects.all()
    return render(request, "core/misprop.html", {'propiedades': propiedades})

def usereg_view(request):
        
    return render(request, "core/usregistrado.html")

def editado_view(request):
    return render(request, "core/editado.html")

def terrenoslistos_view(request):
    return render(request, "core/terrenoslistos.html")

def perfil_view(request):
    sp_user = None
    sp_user_id = request.session.get('sp_user_id')
    if sp_user_id:
       sp_user = SpUsuario.objects.filter(usuario_id=sp_user_id).first()

    return render(request, "core/perfil.html", {'sp_user': sp_user})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.db import transaction, IntegrityError 
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistroForm, LoginForm, PropiedadForm
from .models import SpUsuario, SpPropiedad

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
                request.session['sp_user_rol'] = (u.rol or '').upper()
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

# CREAR PROPIEDAD
def createform_view(request):
    if request.method == "POST":
        form = PropiedadForm(request.POST, request.FILES)
        if form.is_valid():
            propiedad = form.save(commit=False)

            # ID del usuario logueado desde la sesión
            user_id = request.session.get('sp_user_id')
            if user_id is not None:
                propiedad.usuario_id = int(user_id)

            propiedad.save()
            messages.success(request, "Propiedad creada correctamente.")
            return redirect('core:propiedadcrud')   # o 'core:misprop', como prefieras
    else:
        form = PropiedadForm()

    return render(request, 'core/createform.html', {
        'form': form,
        'object': None,   # para que el template sepa que es creación
    })

#EDITAR PROPIEDAD
def editarform_view(request, pk):
    propiedad = get_object_or_404(SpPropiedad, pk=pk)

    if request.method == 'POST':
        form = PropiedadForm(request.POST, request.FILES, instance=propiedad)
        if form.is_valid():
            form.save()
            
            return redirect('core:misprop')
    else:
        form = PropiedadForm(instance=propiedad)

    return render(request, 'core/createform.html', {
        'form': form,
        'object': propiedad,
    })




# LISTAR PROPIEDAD (PARA EDITER Y ELIMINAR)
def misprop_view(request):
    user_id = request.session.get('sp_user_id')
    user_rol = request.session.get('sp_user_rol')

    # Base: todas las propiedades
    propiedades = SpPropiedad.objects.all().order_by('direccion')
    # Si quieres seguir usando ESTADO para otras cosas, puedes dejar:
    # propiedades = SpPropiedad.objects.exclude(estado='INACTIVA').order_by('direccion')

    # Si NO es Admin → se filtra solo por las propiedades del usuario logueado
    if user_rol != 'ADMIN':   # O 'ADMIN' si así está guardado en la BD
        if user_id is not None:
            propiedades = propiedades.filter(usuario_id=int(user_id))
        else:
            propiedades = SpPropiedad.objects.none()

    return render(request, 'core/misprop.html', {
        'propiedades': propiedades,
        'user_rol': user_rol,
    })


    # LISTAR PROPIEDAD SOLO VER
def ver_propiedades_view(request):
    user_id = request.session.get('sp_user_id')
    user_rol = request.session.get('sp_user_rol')

    qs = SpPropiedad.objects.exclude(estado='INACTIVA')

    if user_rol == 'ADMIN':
        propiedades = qs.order_by('direccion')
    else:
        if user_id is not None:
            propiedades = qs.filter(usuario_id=int(user_id)).order_by('direccion')
        else:
            propiedades = SpPropiedad.objects.none()

    return render(request, 'core/ver-propiedades.html', {
        'propiedades': propiedades,
        'user_rol': user_rol,   # por si quieres mostrar algo distinto a futuro
    })



#ELIMINAR (SOLO ADMIN)
def propiedad_delete_view(request, pk):
    user_rol = request.session.get('sp_user_rol')

    if user_rol != 'ADMIN':
        messages.error(request, 'No tienes permisos para eliminar propiedades.')
        return redirect('core:misprop')

    propiedad = get_object_or_404(SpPropiedad, pk=pk)

    if request.method == 'POST':
        propiedad.delete()
        messages.success(request, 'La propiedad fue eliminada correctamente.')
        return redirect('core:misprop')

    return render(request, 'core/propiedad_confirm_delete.html', {
        'propiedad': propiedad
    })

def usereg_view(request):
        
    return render(request, "core/usregistrado.html")

def editado_view(request):
    return render(request, "core/editado.html")

def terrenoslistos_view(request):
    return render(request, "core/terrenoslistos.html")

def perfil_view(request):

    usuario = None #se usa como valor por defecto

    usuario_id = request.session.get('usuario_id')

    if usuario_id:
        try:
            usuario = SpUsuario.objects.get(pk=usuario_id)

        except SpUsuario.DoesNotExist:
            pass #si no existe, usuario queda como None

    #CODIGO OFICIAL (HASTA AHORA)
    #sp_user = None
    #sp_user_id = request.session.get('sp_user_id')
    #if sp_user_id:
       #sp_user = SpUsuario.objects.filter(usuario_id=sp_user_id).first()

    return render(request, "core/perfil.html", {'usuario': usuario})


def logout_views(request):
    logout(request)
    messages.info(request, "Se ha cerrado la sesion")
    return redirect('core:index')


#PARA ELIMINAR PROPIEDAD (PROBAR AUN!!)
def propiedadeliminar_view(request, pk):
    propiedad = get_object_or_404(SpPropiedad, pk=pk)

    if request.method == 'POST':
        propiedad.delete()
        messages.success(request, "La propiedad se ha eliminado correctamente")
        return redirect('core:misprop')
    
    return render(request, 'core/propiedad_confirm_delete.html', {'propiedad': propiedad})









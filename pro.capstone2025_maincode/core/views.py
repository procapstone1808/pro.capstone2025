from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .forms import RegistroForm, LoginForm
from .models import SpUsuario

# Create your views here.

def index(request):
    return render(request, "core/index.html")


def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # Duplicidad (RUT y Email)
            if SpUsuario.objects.filter(rut=cd['rut']).exists():
                form.add_error('rut', 'Ya existe un usuario con este RUT.')
            elif SpUsuario.objects.filter(email__iexact=cd['email']).exists():
                form.add_error('email', 'Ya existe un usuario con este email.')
            else:
                with transaction.atomic():
                    SpUsuario.objects.create(
                        rut=cd['rut'].strip(),
                        nombre=cd['nombre'].strip(),
                        email=cd['email'].strip(),
                        telefono=(cd.get('telefono') or '').strip(),
                        rol=cd['rol'],   # plano (simple)
                        is_active='Y',
                        password=cd['password']
                    )
                # Guarda datos mínimos en sesión y redirige (REVISAR )
                u = SpUsuario.objects.get(rut=cd['rut'])
                request.session['sp_user_id'] = int(u.usuario_id)
                request.session['sp_user_nombre'] = u.nombre
                request.session['sp_user_rol'] = u.rol
                messages.success(request, "¡Registro exitoso!")
                return redirect('core:main_registrado')
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
                password=cd['password'],   
                is_active='Y'
            ).first()
            if u:
                request.session['sp_user_id'] = int(u.usuario_id)
                request.session['sp_user_nombre'] = u.nombre
                request.session['sp_user_rol'] = u.rol
                messages.success(request, f"Bienvenido, {u.nombre}.")
                return redirect('core:main_registrado')
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
    messages.info(request, "Has cerrado sesión.")
    return redirect('core:index')


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

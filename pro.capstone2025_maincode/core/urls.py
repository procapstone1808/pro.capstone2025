from django.urls import path
from .views import index, login_view, registro_view, ayuda_view, nosotros_view, propiedad_view, salir, mainregistrado_view,  gestordocumentos_view, propiedades_view, propiedadform_view

app_name = 'core'
urlpatterns = [ 
    path('', index, name='index'),
    path("login/", login_view, name="login"),
    path("registro/", registro_view, name="registro"),
    path('salir/', salir, name='salir'),
    path("ayuda/", ayuda_view, name="ayuda"), 
    path("nosotros/", nosotros_view, name="nosotros"), 
    path("main-registrado/", mainregistrado_view, name="main-registrado"),
    path("propiedades/", propiedades_view, name="propiedades"),
    path("gestor-documentos/", gestordocumentos_view, name="gestor-documentos"),
    path("propiedadcrud/", propiedad_view, name="propiedad"), 
    path("propiedadform/", propiedadform_view, name="propiedadform"),

    


]
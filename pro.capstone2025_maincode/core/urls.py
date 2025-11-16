from django.urls import path
from .views import index, login_view, registro_view, usereg_view, ayuda_view, nosotros_view, propiedad_view, salir, mainregistrado_view,  gestordocumentos_view, propiedades_view, propiedadform_view, propiedadform_usreg_view, editarform_view, misprop_view, PropiedadUpdateView, EditarPropiedadView

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
    path("propiedadcrud/", propiedad_view, name="propiedadcrud"), 
    path("propiedadform/", propiedadform_view, name="propiedadform"),
    path("propiedadform-usreg/", propiedadform_usreg_view, name="propiedadform_usreg"),
    path("editar-propform/", editarform_view, name="editar-propform"),
    path("propiedades/<int:pk>/editar/", PropiedadUpdateView.as_view(), name="propiedad_editar"),
    path("propiedades/<int:pk>/editar-form/", EditarPropiedadView.as_view(), name="propiedad_editar_form"),
    path("misprop/", misprop_view, name="misprop"),
    path("usregistrado/", usereg_view, name="usregistrado"),
    
    #path("propiedades/<int:pk>/editar/", PropiedadUpdateView.as_view(), name="propiedad_editar"),

    


]
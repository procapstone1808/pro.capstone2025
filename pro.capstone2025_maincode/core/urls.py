from django.urls import path
from .views import index, login_view, registro_view, usereg_view, editado_view, ayuda_view, nosotros_view, propiedad_view, terrenoslistos_view, perfil_view, salir, mainregistrado_view, gestordocumentos_view, logout_views, propiedades_view, propiedadform_usreg_view, createform_view, editarform_view, misprop_view

app_name = 'core'
urlpatterns = [ 
    path('', index, name='index'),
    path("login/", login_view, name="login"),
    path("registro/", registro_view, name="registro"),
    path('salir/', salir, name='salir'),
    path("ayuda/", ayuda_view, name="ayuda"), 
    path("nosotros/", nosotros_view, name="nosotros"), 
    path("main-registrado/", mainregistrado_view, name="main-registrado"),
    path("gestor-documentos/", gestordocumentos_view, name="gestor-documentos"),
    path("propiedadcrud/", propiedad_view, name="propiedadcrud"), 
    path("createform/", createform_view, name="createform"), #CREAR PROPIEDADES
    path("misprop/", misprop_view, name="misprop"), #LISTAR PROPIEDADES
    path("misprop/<int:pk>/editarform/", editarform_view, name="editarform"),#EDITAR PROPIEDADES
    #path("misprop/<int:pk>/eliminar/", propiedad_delete_view, name="propiedad_eliminar"), #ELIMINAR PROPIEDADES (CAMBIO DE ESTADO)



    path("usregistrado/", usereg_view, name="usregistrado"),
    path("editado/", editado_view, name="editado"),
    path("terrenoslistos/", terrenoslistos_view, name="terrenoslistos"),
    path("perfil/", perfil_view, name="perfil"),
    path("logout/", logout_views, name="logout"),
    
    

]
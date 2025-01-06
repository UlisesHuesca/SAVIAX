from django.urls import path
from . import views


urlpatterns = [
    path('entradas/pendientes_entrada', views.pendientes_entrada, name='pendientes-entrada'),
    path('producto-terminado-entrada/', views.productos_terminados_entrada, name='producto-terminado-entrada'),
    path('validar-entrada-terminado/<int:pk>/', views.validar_entrada_terminado, name='validar-entrada-terminado'),
    path('no-validar-entrada-terminado/<int:pk>/', views.no_validar_entrada_terminado, name='no-validar-entrada-terminado'),
    path("producto_terminado_componentes/<int:pk>/", views.producto_terminado_componente_ver, name="producto_terminado_componente_ver"),
    path('producto-terminado-salida/', views.productos_terminados_salida, name='producto-terminado-salida'),
    path("producto_terminado_salida_cliente/<int:pk>/", views.terminado_salida_editar_cliente, name="terminado_salida_editar_cliente"),



    path('entradas/pendientes_entrada/articulos/<int:pk>', views.articulos_entrada, name='articulos_entrada'),
    path('entradas/pendientes_recepcion/articulos/<int:pk>', views.articulos_recepcion, name='articulos_recepcion'),
    #path('update_entrada/', views.update_entrada, name='update-entrada'),
    path('update_recepcion/', views.update_recepcion_articulos, name='update-recepcion'),
    path('entradas/pendientes_calidad', views.pendientes_calidad, name='pendientes_calidad'),
    path('entradas/pendientes_calidad/reporte/<int:pk>', views.reporte_calidad, name='reporte_calidad'),
    path('entradas/devolucion_a_proveedor/', views.devolucion_a_proveedor, name='devolucion_a_proveedor'),
    path('entradas/no_conformidad/<int:pk>', views.no_conformidad, name='no-conformidad'),
    path('entradas/no_conformidad_almacen/<int:pk>', views.no_conformidad_almacen, name='no-conformidad-almacen'),
    path('entradas/productos/<int:pk>', views.productos, name="productos"),
    path('no_conformidad/', views.update_no_conformidad, name="update_no_conformidad"),
    path('entradas/recepcion', views.pendientes_recepcion, name='pendientes-recepcion'),
    path('entradas/recepcion_servicios', views.recepcion_servicios, name='recepcion-servicios'),
    path('entradas/articulos_recepcion_servicios/<int:pk>', views.articulos_recepcion_servicios, name='articulos-recepcion-servicios'),
    path('update_cantidad/', views.update_cantidad, name='update_cantidad'),
    path('update_fecha/', views.update_fecha, name='update_fecha'),
    path('productos/nc/<int:pk>', views.productos_nc, name="productos_nc"),
    path('entradas/nc', views.entradas_nc, name='entradas_nc'),
    path('cierre/nc/<int:pk>', views.cierre_nc, name="cierre_nc"),
    path('entradas/caducidad', views.entradas_con_caducidad, name='entradas_caducidad'),
    path('calidad/entradas', views.calidad_entradas, name='calidad_entradas'),
    path('calidad/update_comentario/', views.update_comentario, name='update_comentario'),
    path('actualizar_calidad/', views.autorizar_calidad, name='autorizar_calidad'),
    path('calidad/entradas/autorizadas', views.calidad_entradas_autorizadas, name='calidad_entradas_autorizadas'),

]
from django.urls import path
from . import views


urlpatterns = [
    path('entradas/pendientes_entrada', views.pendientes_entrada, name='pendientes-entrada'),
    path('entradas/pendientes_entrada/articulos/<int:pk>', views.articulos_entrada, name='articulos_entrada'),
    path('entradas/pendientes_recepcion/articulos/<int:pk>', views.articulos_recepcion, name='articulos_recepcion'),
    #path('update_entrada/', views.update_entrada, name='update-entrada'),
    path('update_recepcion/', views.update_recepcion_articulos, name='update-recepcion'),
    path('entradas/pendientes_calidad', views.pendientes_calidad, name='pendientes_calidad'),
    path('entradas/pendientes_calidad/reporte/<int:pk>', views.reporte_calidad, name='reporte_calidad'),
    path('entradas/devolucion_a_proveedor/', views.devolucion_a_proveedor, name='devolucion_a_proveedor'),
    path('entradas/no_conformidad/<int:pk>', views.no_conformidad, name='no-conformidad'),
    path('entradas/productos/<int:pk>', views.productos, name="productos"),
    path('no_conformidad/', views.update_no_conformidad, name="update_no_conformidad"),
    path('entradas/recepcion', views.pendientes_recepcion, name='pendientes-recepcion'),
    path('update_cantidad/', views.update_cantidad, name='update_cantidad'),
]
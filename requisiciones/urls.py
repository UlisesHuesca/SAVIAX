from django.urls import path, include
from . import views


urlpatterns = [
    path('sol_autorizadas/', views.solicitud_autorizada, name='solicitud-autorizada'),
    path('editar_cliente/<int:salida_id>/', views.editar_cliente, name='editar_cliente'),

    #path('sol_autorizadas/producto_terminado', views.salidas_producto_terminado, name='salida-producto-terminado'),
    path('sol_autorizadas_pendientes/', views.solicitudes_autorizadas_pendientes, name='solicitudes-autorizadas-pendientes'),
    path('salida_material/<int:pk>/', views.salida_material, name='salida-material'),
    path('salida_material_externo/<int:pk>/', views.salida_material_externo, name='salida-material-externo'),
    path('devolucion_material/<int:pk>/', views.devolucion_material, name='devolucion-material'),
    path('devolucion_salida/<int:pk>/', views.devolucion_material_salida, name='devolucion-material-salida'),
    path('devolucion/matriz_autorizar', views.matriz_autorizar_devolucion, name='matriz-autorizar-devolucion'),
    path('devolucion/autorizar/<int:pk>/', views.autorizar_devolucion, name='autorizar-devolucion'),
    path('devolucion/cancelar/<int:pk>/', views.cancelar_devolucion, name='cancelar-devolucion'),
    path('update_requi/', views.update_requisicion, name='update-requi'), #########################
    path('update_salida/', views.update_salida, name='update-salida'),
    path('update_devolucion/', views.update_devolucion, name='update-devolucion'),
    path('update_devolucion_salida/', views.update_devolucion_salida, name='update-devolucion-salida'),
    path('sol_autorizadas/firma', views.solicitud_autorizada_firma, name='solicitud-autorizada-firma'),
    path('salida_material/firma/<int:pk>/', views.salida_material_usuario, name='salida-material-usuario'),
    path('sol_autorizadas_orden/', views.solicitud_autorizada_orden, name='solicitud-autorizada-orden'),
    path('matriz_salida_activos/', views.matriz_salida_activos, name='matriz-salida-activos'),
    path('autorizacion/', views.requisicion_autorizacion, name='requisicion-autorizacion'),
    path('sol_autorizadas_orden/detalle/<int:pk>/', views.detalle_orden, name='detalle-orden'),
    path('sol_autorizadas_orden/requisicion_detalle/<int:pk>/', views.requisicion_detalle, name='requisicion-detalle'), ###############
    path('sol_autorizadas_orden/liberar_stock/<int:pk>/', views.liberar_stock, name='liberar-stock'),
    path('sol_autorizadas_orden/requisicion_creada/<int:pk>/', views.requisicion_creada_detalle, name='requisicion-creada-detalle'),
    path('sol_autorizadas_orden/requisicion_autorizar/<int:pk>/', views.requisicion_autorizar, name='requisicion-autorizar'),
    path('sol_autorizadas_orden/requisicion_cancelar/<int:pk>/', views.requisicion_cancelar, name='requisicion-cancelar'),
    path('salida_material/solicitud_pdf/<int:pk>/', views.render_pdf_view, name='solicitud-pdf'),
    path('reporte_entradas/', views.reporte_entradas, name='reporte-entradas'),
    path('reporte_salidas/', views.reporte_salidas, name='reporte-salidas'),


    #path('inventario/upload_batch_inventario', views.upload_batch_inventario, name='upload_batch_inventario'),
    path('inventario/historico_articulos_para_surtir/', views.historico_articulos_para_surtir, name='historico-articulos-para-surtir'),
    path('salidas/historico_salidas/', views.historico_salidas, name='historico-salidas'),
    path('salida_material/salida_pdf/<int:pk>/', views.render_salida_pdf, name='vale-salida-pdf'),
    path('entrada_material/entrada_pdf/<int:pk>/', views.render_entrada_pdf, name='vale-entrada-pdf'),

    path('requisiciones/estatus', views.requisiciones_status, name='requisiciones-status'),
    path('requisicion_pdf/<int:pk>/', views.render_requisicion_pdf_view, name='requisicion-pdf'),
    path('matriz/devolucion_ordenes', views.reporte_devoluciones, name='devolucion_ordenes'),
    
    path('salida_producto_terminado_crear/<int:pk>/', views.terminado_salida_surtir, name='salida_producto_terminado_crear'),
    ]
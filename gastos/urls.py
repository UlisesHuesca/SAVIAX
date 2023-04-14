from django.urls import path
from . import views


urlpatterns = [
    path('gasto/crear_gasto', views.crear_gasto, name='crear-gasto'),
    path('update_gasto/', views.update_gasto, name='update-gasto'),
    path('gasto/editar_gasto/<int:pk>/', views.editar_gasto, name='editar-gasto'),
    path('gasto/solicitudes_gasto/', views.solicitudes_gasto, name='solicitudes-gasto'),
    path('gasto/detalle_gastos/<int:pk>/', views.detalle_gastos, name='detalle-gastos'),
    path('gasto/gastos_pendientes_autorizar/', views.gastos_pendientes_autorizar, name='gastos-pendientes-autorizar'),
    path('gasto/autorizar_gasto/<int:pk>/', views.autorizar_gasto, name = 'autorizar-gasto'),
    path('gasto/cancelar_gasto/<int:pk>/', views.cancelar_gasto, name='cancelar-gasto'),
    path('gasto/pago_gastos_autorizados/', views.pago_gastos_autorizados, name='pago-gastos-autorizados'),
    path('gasto/pago_gasto/<int:pk>/', views.pago_gasto, name='pago-gasto'),
    ]
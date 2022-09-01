from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('entradas/pendientes_entrada', views.pendientes_entrada, name='pendientes_entrada'),
    path('entradas/pendientes_entrada/articulos/<int:pk>', views.articulos_entrada, name='articulos_entrada'),
    path('update_entrada/', views.update_entrada, name='update-entrada'),
    ]
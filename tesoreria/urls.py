from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('tesoreria/compras_autorizadas', views.compras_autorizadas, name='compras-autorizadas'),
    path('tesoreria/compras_autorizadas/pagos/<int:pk>/', views.compras_pagos, name='compras-pagos'),
    path('tesoreria/matriz_pagos/', views.matriz_pagos, name='matriz-pagos'),
    ]
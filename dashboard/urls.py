from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.index, name= 'dashboard-index'),
    path('staff/', views.staff, name='dashboard-staff'),
    path('product/', views.product, name='dashboard-product'),
    path('product/upload_batch_products', views.upload_batch_products, name='upload_batch_products'),
    path('order/', views.order, name='dashboard-order'),
    path('product/delete/<int:pk>/', views.product_delete, name='dashboard-product-delete'),
    path('product/update/<int:pk>/', views.product_update, name='dashboard-product-update'),
    path('product/add/', views.add_product, name='add-product'),
    path('ajax/load-subfamilias/', views.load_subfamilias, name='ajax_load_subfamilias'),  # <-- rutina en Ajax
    path('dashboard/staff_detail/<int:pk>/', views.staff_detail, name='dashboard-staff-detail'),
]


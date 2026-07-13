from django.urls import path
from . import views

urlpatterns = [
    path('stitching/', views.stitching_list, name='stitching_list'),
    path('stitching/add/', views.stitching_add, name='stitching_add'),
    path('stitching/<int:pk>/', views.stitching_detail, name='stitching_detail'),
    path('stitching/edit/<int:pk>/', views.stitching_edit, name='stitching_edit'),
    path('stitching/delete/<int:pk>/', views.stitching_delete, name='stitching_delete'),
    path('stitching/get-size-measurements/', views.get_size_measurements, name='get_size_measurements'),
    path('stitching/get-customer-measurements/', views.get_customer_measurements, name='get_customer_measurements'),
]
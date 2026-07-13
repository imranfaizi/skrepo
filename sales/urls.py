from django.urls import path
from . import views

urlpatterns = [
    path('sales/', views.sale_list, name='sale_list'),
    path('sales/add/', views.sale_add, name='sale_add'),
    path('sales/returns/', views.sale_return_list, name='sale_return_list'),
    path('sales/returns/<int:pk>/', views.sale_return_invoice, name='sale_return_invoice'),
    path('sales/customer-search/', views.customer_search, name='customer_search'),
    path('sales/<int:pk>/', views.sale_detail, name='sale_detail'),
    path('sales/<int:pk>/edit/', views.sale_edit, name='sale_edit'),
    path('sales/<int:pk>/delete/', views.sale_delete, name='sale_delete'),
    path('sales/<int:sale_id>/return/', views.sale_return_create, name='sale_return_create'),
]
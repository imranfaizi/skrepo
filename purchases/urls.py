from django.urls import path
from . import views

urlpatterns = [
    path('purchases/', views.purchase_list, name='purchase_list'),
    path('purchases/add/', views.purchase_add, name='purchase_add'),
    path('purchases/<int:pk>/', views.purchase_detail, name='purchase_detail'),
    path('purchases/<int:pk>/payment/', views.purchase_payment, name='purchase_payment'),
    path('purchases/<int:pk>/delete/', views.purchase_delete, name='purchase_delete'),
]
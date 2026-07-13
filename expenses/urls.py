from django.urls import path
from . import views

urlpatterns = [
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/add/', views.expense_add, name='expense_add'),
    path('expenses/edit/<int:pk>/', views.expense_edit, name='expense_edit'),
    path('expenses/delete/<int:pk>/', views.expense_delete, name='expense_delete'),

    path('expense-categories/', views.category_list, name='expense_category_list'),
    path('expense-categories/add/', views.category_add, name='expense_category_add'),
    path('expense-categories/delete/<int:pk>/', views.category_delete, name='expense_category_delete'),
]
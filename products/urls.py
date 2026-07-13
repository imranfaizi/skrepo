from django.urls import path
from . import views

urlpatterns = [
    # Products
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('products/delete/<int:pk>/', views.product_delete, name='product_delete'),

    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),

    # Sub Categories
    path('subcategories/', views.subcategory_list, name='subcategory_list'),
    path('subcategories/add/', views.subcategory_add, name='subcategory_add'),
    path('subcategories/delete/<int:pk>/', views.subcategory_delete, name='subcategory_delete'),

    # Manufacturers
    path('manufacturers/', views.manufacturer_list, name='manufacturer_list'),
    path('manufacturers/add/', views.manufacturer_add, name='manufacturer_add'),
    path('manufacturers/delete/<int:pk>/', views.manufacturer_delete, name='manufacturer_delete'),
]
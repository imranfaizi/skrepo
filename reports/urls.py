from django.urls import path
from . import views

urlpatterns = [
    path('reports/', views.reports_home, name='reports_home'),
    path('reports/sales/', views.sales_report, name='sales_report'),
    path('reports/purchases/', views.purchases_report, name='purchases_report'),
    path('reports/expenses/', views.expenses_report, name='expenses_report'),
    path('reports/profit-loss/', views.profit_loss_report, name='profit_loss_report'),
    path('reports/inventory/', views.inventory_report, name='inventory_report'),
    path('reports/export/sales/', views.export_sales_csv, name='export_sales_csv'),
    path('reports/export/purchases/', views.export_purchases_csv, name='export_purchases_csv'),
    path('reports/export/expenses/', views.export_expenses_csv, name='export_expenses_csv'),
]
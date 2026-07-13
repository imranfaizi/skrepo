from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login / Logout
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Apps
    path('', include('dashboard.urls')),
    path('', include('products.urls')),
    path('', include('suppliers.urls')),
    path('', include('purchases.urls')),
    path('', include('sales.urls')),
    path('', include('customers.urls')),
    path('', include('stitching.urls')),
    path('', include('expenses.urls')),
    path('', include('reports.urls')),
]
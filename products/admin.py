from django.contrib import admin
from .models import Category, SubCategory, Manufacturer, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_at']
    search_fields = ['name']
    list_filter = ['category']

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_code', 'category', 'stock', 'purchase_price', 'sale_price', 'is_active']
    search_fields = ['name', 'product_code']
    list_filter = ['category', 'is_active', 'unit_type']
    list_editable = ['is_active']
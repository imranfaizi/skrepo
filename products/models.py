from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    class Meta:
        verbose_name_plural = "Sub Categories"


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    UNIT_CHOICES = [
        ('quantity', 'By Quantity'),
        ('meters', 'By Meters'),
    ]

    name = models.CharField(max_length=200)
    product_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True, blank=True)
    unit_type = models.CharField(max_length=20, choices=UNIT_CHOICES, default='quantity')
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_alert = models.DecimalField(max_digits=10, decimal_places=2, default=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def profit_percentage(self):
        if self.purchase_price > 0:
            profit = self.sale_price - self.purchase_price
            return round((profit / self.purchase_price) * 100, 2)
        return 0

    @property
    def is_low_stock(self):
        return self.stock <= self.stock_alert

from django.db import models
from products.models import Product
from customers.models import Customer


class Sale(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('easypaisa', 'EasyPaisa'),
        ('jazzcash', 'JazzCash'),
        ('bank', 'Bank Transfer'),
        ('credit', 'Credit'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sales'
    )
    invoice_number = models.CharField(max_length=100, unique=True)
    sale_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='cash'
    )
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale #{self.invoice_number}"

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def net_total(self):
        return self.subtotal - self.discount

    @property
    def total_profit(self):
        return sum(item.profit for item in self.items.all())


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.sale_price * self.quantity

    @property
    def profit(self):
        return (self.sale_price - self.purchase_price) * self.quantity

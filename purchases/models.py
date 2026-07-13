from django.db import models
from suppliers.models import Supplier
from products.models import Product


class PurchaseInvoice(models.Model):
    STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
    ]

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchase_invoices')
    invoice_number = models.CharField(max_length=100, unique=True)
    invoice_date = models.DateField()
    due_date = models.DateField(blank=True, null=True)
    reference_no = models.CharField(max_length=100, blank=True, null=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unpaid')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice #{self.invoice_number}"

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def net_total(self):
        return self.subtotal

    @property
    def balance(self):
        return self.net_total - self.paid_amount

    def update_status(self):
        if self.paid_amount <= 0:
            self.status = 'unpaid'
        elif self.paid_amount >= self.net_total:
            self.status = 'paid'
        else:
            self.status = 'partial'
        self.save()


class PurchaseItem(models.Model):
    invoice = models.ForeignKey(PurchaseInvoice, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total_price(self):
        price = self.purchase_price * self.quantity
        discount_amount = (price * self.discount) / 100
        return price - discount_amount

    @property
    def profit_percentage(self):
        if self.purchase_price > 0:
            profit = self.product.sale_price - self.purchase_price
            return round((profit / self.purchase_price) * 100, 2)
        return 0
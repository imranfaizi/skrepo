from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    business_name = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def total_invoices(self):
        try:
            return self.purchase_invoices.count()
        except:
            return 0

    @property
    def total_amount(self):
        try:
            return sum(inv.net_total for inv in self.purchase_invoices.all())
        except:
            return 0

    @property
    def total_paid(self):
        try:
            return sum(inv.paid_amount for inv in self.purchase_invoices.all())
        except:
            return 0

    @property
    def total_balance(self):
        return self.total_amount - self.total_paid
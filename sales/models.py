from django.db import models
from django.contrib.auth.models import User
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
    invoice_number  = models.CharField(max_length=100, unique=True)
    sale_date       = models.DateTimeField(auto_now_add=True)
    payment_method  = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash')
    discount        = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    advance_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes           = models.TextField(blank=True, null=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale #{self.invoice_number}"

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def discount_amount(self):
        return round((self.subtotal * self.discount) / 100, 2)

    @property
    def net_total(self):
        return round(self.subtotal - self.discount_amount, 2)

    @property
    def balance(self):
        return round(self.net_total - self.advance_payment, 2)

    @property
    def total_profit(self):
        raw_profit = sum(item.profit for item in self.items.all())
        return round(raw_profit - self.discount_amount, 2)


class SaleItem(models.Model):
    sale                = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product             = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    custom_product_name = models.CharField(max_length=255, blank=True, null=True)
    quantity            = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price          = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price      = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        name = self.custom_product_name if self.custom_product_name else self.product.name if self.product else '-'
        return f"{name} x {self.quantity}"

    @property
    def product_display_name(self):
        if self.custom_product_name:
            return self.custom_product_name
        return self.product.name if self.product else "-"

    @property
    def total_price(self):
        return round(self.sale_price * self.quantity, 2)

    @property
    def profit(self):
        return round((self.sale_price - self.purchase_price) * self.quantity, 2)


class SaleReturn(models.Model):
    RETURN_TYPE = [
        ('refund',     'Return with Refund'),
        ('adjustment', 'Return with Adjustment'),
        ('exchange',   'Exchange with Product'),
    ]
    sale            = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='returns')
    return_type     = models.CharField(max_length=20, choices=RETURN_TYPE)
    date            = models.DateTimeField(auto_now_add=True)
    notes           = models.TextField(blank=True)
    refund_amount   = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    exchange_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_balance     = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_by      = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Return #{self.pk} → Sale #{self.sale.pk}"


class SaleReturnItem(models.Model):
    sale_return = models.ForeignKey(SaleReturn, on_delete=models.CASCADE, related_name='returned_items')
    product     = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    custom_name = models.CharField(max_length=200, blank=True)
    quantity    = models.DecimalField(max_digits=10, decimal_places=2)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    total       = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.price
        super().save(*args, **kwargs)


class SaleExchangeItem(models.Model):
    sale_return = models.ForeignKey(SaleReturn, on_delete=models.CASCADE, related_name='exchange_items')
    product     = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    custom_name = models.CharField(max_length=200, blank=True)
    quantity    = models.DecimalField(max_digits=10, decimal_places=2)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    total       = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.price
        super().save(*args, **kwargs)
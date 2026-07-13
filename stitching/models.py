from django.db import models
from products.models import Product
from customers.models import Customer


class StitchingOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('delivered', 'Delivered'),
    ]

    SIZE_CHOICES = [
        # Kids
        ('20', 'Size 20 (Age 2-3)'),
        ('22', 'Size 22 (Age 4-5)'),
        ('24', 'Size 24 (Age 6-7)'),
        ('26', 'Size 26 (Age 8-9)'),
        ('28', 'Size 28 (Age 10-11)'),
        ('30', 'Size 30 (Age 12-13)'),
        # Adults
        ('32', 'Size 32 (XS)'),
        ('34', 'Size 34 (S)'),
        ('36', 'Size 36 (M)'),
        ('38', 'Size 38 (L)'),
        ('40', 'Size 40 (XL)'),
        ('42', 'Size 42 (XXL)'),
        ('44', 'Size 44 (3XL)'),
        ('46', 'Size 46 (4XL)'),
        ('custom', 'Custom Size'),
    ]

    # Basic Info
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stitching_orders'
    )
    customer_name  = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    code_number    = models.CharField(max_length=100, blank=True, null=True)
    fabric = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stitching_orders'
    )
    fabric_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stitching_cost  = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    advance_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_date      = models.DateField(auto_now_add=True)
    delivery_date   = models.DateField(blank=True, null=True)
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes           = models.TextField(blank=True, null=True)

    # Size
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, blank=True, null=True)

    # Kameez Measurements
    shirt_length  = models.CharField(max_length=20, blank=True, null=True)
    shoulder      = models.CharField(max_length=20, blank=True, null=True)
    chest         = models.CharField(max_length=20, blank=True, null=True)
    waist         = models.CharField(max_length=20, blank=True, null=True)
    sleeve_length = models.CharField(max_length=20, blank=True, null=True)
    collar        = models.CharField(max_length=20, blank=True, null=True)

    # Shalwar Measurements
    shalwar_length = models.CharField(max_length=20, blank=True, null=True)
    shalwar_waist  = models.CharField(max_length=20, blank=True, null=True)
    hip            = models.CharField(max_length=20, blank=True, null=True)
    bottom_width   = models.CharField(max_length=20, blank=True, null=True)

    # Extra/Other Measurements
    extra_measurements = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def balance(self):
        return self.stitching_cost - self.advance_payment

    def __str__(self):
        return f"Order #{self.pk} - {self.customer_name}"
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal
from .models import PurchaseInvoice, PurchaseItem
from suppliers.models import Supplier
from products.models import Product


@login_required
def purchase_list(request):
    invoices = PurchaseInvoice.objects.all().order_by('-created_at')
    total_amount = sum(inv.net_total for inv in invoices)
    total_paid = sum(inv.paid_amount for inv in invoices)
    total_balance = total_amount - total_paid
    return render(request, 'purchases/purchase_list.html', {
        'invoices': invoices,
        'total_amount': total_amount,
        'total_paid': total_paid,
        'total_balance': total_balance,
    })


@login_required
def purchase_add(request):
    suppliers = Supplier.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True)

    if request.method == 'POST':
        supplier_id = request.POST.get('supplier')
        invoice_number = request.POST.get('invoice_number')
        invoice_date = request.POST.get('invoice_date')
        due_date = request.POST.get('due_date') or None
        reference_no = request.POST.get('reference_no') or None
        notes = request.POST.get('notes') or None

        # Check duplicate invoice number
        if PurchaseInvoice.objects.filter(invoice_number=invoice_number).exists():
            messages.error(request, 'Invoice number already exists.')
            return render(request, 'purchases/purchase_add.html', {
                'suppliers': suppliers,
                'products': products,
            })

        # Create invoice
        invoice = PurchaseInvoice.objects.create(
            supplier_id=supplier_id,
            invoice_number=invoice_number,
            invoice_date=invoice_date,
            due_date=due_date,
            reference_no=reference_no,
            notes=notes,
        )

        # Add items
        product_ids = request.POST.getlist('product_id[]')
        quantities = request.POST.getlist('quantity[]')
        prices = request.POST.getlist('purchase_price[]')
        discounts = request.POST.getlist('discount[]')

        for i in range(len(product_ids)):
            if product_ids[i]:
                product = Product.objects.get(pk=product_ids[i])
                qty = Decimal(str(quantities[i] or 0))
                price = Decimal(str(prices[i] or 0))
                discount = Decimal(str(discounts[i] or 0))

                PurchaseItem.objects.create(
                    invoice=invoice,
                    product=product,
                    quantity=qty,
                    purchase_price=price,
                    discount=discount,
                )

                # Update stock
                product.stock += qty
                product.purchase_price = price
                product.save()

        messages.success(request, f'Purchase invoice #{invoice_number} created successfully.')
        return redirect('purchase_list')

    # Auto generate invoice number
    last_invoice = PurchaseInvoice.objects.order_by('-id').first()
    next_number = f'INV-{(last_invoice.id + 1 if last_invoice else 1):04d}'

    return render(request, 'purchases/purchase_add.html', {
        'suppliers': suppliers,
        'products': products,
        'next_number': next_number,
        'today': timezone.now().date(),
    })


@login_required
def purchase_detail(request, pk):
    invoice = get_object_or_404(PurchaseInvoice, pk=pk)
    return render(request, 'purchases/purchase_detail.html', {'invoice': invoice})


@login_required
def purchase_payment(request, pk):
    invoice = get_object_or_404(PurchaseInvoice, pk=pk)
    if request.method == 'POST':
        amount = Decimal(str(request.POST.get('amount') or 0))
        invoice.paid_amount += amount
        if invoice.paid_amount > invoice.net_total:
            invoice.paid_amount = invoice.net_total
        invoice.update_status()
        messages.success(request, f'Payment of Rs. {amount} recorded successfully.')
        return redirect('purchase_list')
    return render(request, 'purchases/purchase_payment.html', {'invoice': invoice})


@login_required
def purchase_delete(request, pk):
    invoice = get_object_or_404(PurchaseInvoice, pk=pk)
    # Reverse stock
    for item in invoice.items.all():
        item.product.stock -= item.quantity
        item.product.save()
    invoice.delete()
    messages.success(request, 'Purchase invoice deleted successfully.')
    return redirect('purchase_list')
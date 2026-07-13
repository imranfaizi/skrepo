from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal
from .models import Sale, SaleItem
from products.models import Product
from customers.models import Customer


@login_required
def sale_list(request):
    sales = Sale.objects.all().order_by('-created_at')
    total_revenue = sum(sale.net_total for sale in sales)
    total_profit = sum(sale.total_profit for sale in sales)
    return render(request, 'sales/sale_list.html', {
        'sales': sales,
        'total_revenue': total_revenue,
        'total_profit': total_profit,
    })


@login_required
def sale_add(request):
    products = Product.objects.filter(is_active=True)
    customers = Customer.objects.all()

    if request.method == 'POST':
        customer_id = request.POST.get('customer') or None
        payment_method = request.POST.get('payment_method')
        discount = Decimal(str(request.POST.get('discount') or 0))
        notes = request.POST.get('notes') or None

        # Auto generate invoice number
        last_sale = Sale.objects.order_by('-id').first()
        invoice_number = f'SALE-{(last_sale.id + 1 if last_sale else 1):04d}'

        # Create sale
        sale = Sale.objects.create(
            customer_id=customer_id,
            invoice_number=invoice_number,
            payment_method=payment_method,
            discount=discount,
            notes=notes,
        )

        # Add items
        product_ids = request.POST.getlist('product_id[]')
        quantities = request.POST.getlist('quantity[]')
        prices = request.POST.getlist('sale_price[]')

        for i in range(len(product_ids)):
            if product_ids[i]:
                product = Product.objects.get(pk=product_ids[i])
                qty = Decimal(str(quantities[i] or 0))
                price = Decimal(str(prices[i] or 0))

                # Check stock
                if product.stock < qty:
                    messages.error(request, f'Insufficient stock for {product.name}.')
                    sale.delete()
                    return redirect('sale_add')

                SaleItem.objects.create(
                    sale=sale,
                    product=product,
                    quantity=qty,
                    sale_price=price,
                    purchase_price=product.purchase_price,
                )

                # Deduct stock
                product.stock -= qty
                product.save()

        messages.success(request, f'Sale #{invoice_number} recorded successfully.')
        return redirect('sale_list')

    return render(request, 'sales/sale_add.html', {
        'products': products,
        'customers': customers,
        'today': timezone.now().date(),
    })


@login_required
def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'sales/sale_detail.html', {'sale': sale})


@login_required
def sale_delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    # Reverse stock
    for item in sale.items.all():
        item.product.stock += item.quantity
        item.product.save()
    sale.delete()
    messages.success(request, 'Sale deleted successfully.')
    return redirect('sale_list')

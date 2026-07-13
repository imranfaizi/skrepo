from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal
from .models import Sale, SaleItem, SaleReturn, SaleReturnItem, SaleExchangeItem
from products.models import Product
from customers.models import Customer


@login_required
def sale_list(request):
    search = request.GET.get('search', '')
    sales  = Sale.objects.all().order_by('-created_at')
    if search:
        sales = sales.filter(invoice_number__icontains=search) | \
                sales.filter(customer__name__icontains=search)
    total_revenue = sum(sale.net_total for sale in sales)
    total_profit  = sum(sale.total_profit for sale in sales)
    return render(request, 'sales/sale_list.html', {
        'sales':         sales,
        'total_revenue': total_revenue,
        'total_profit':  total_profit,
        'search':        search,
    })


@login_required
def sale_add(request):
    products  = Product.objects.filter(is_active=True)
    customers = Customer.objects.all()

    if request.method == 'POST':
        customer_id    = request.POST.get('customer') or None
        payment_method = request.POST.get('payment_method')
        discount       = round(Decimal(str(request.POST.get('discount') or 0)), 2)
        advance        = Decimal(str(request.POST.get('advance_payment') or 0))
        notes          = request.POST.get('notes') or None

        customer_name_input = request.POST.get('customer_name_input', '').strip()
        if not customer_id and customer_name_input:
            customer_obj, _ = Customer.objects.get_or_create(name=customer_name_input)
            customer_id = customer_obj.pk

        last_sale      = Sale.objects.order_by('-id').first()
        invoice_number = f'SALE-{(last_sale.id + 1 if last_sale else 1):04d}'

        sale = Sale.objects.create(
            customer_id     = customer_id,
            invoice_number  = invoice_number,
            payment_method  = payment_method,
            discount        = discount,
            advance_payment = advance,
            notes           = notes,
        )

        product_ids  = request.POST.getlist('product_id[]')
        quantities   = request.POST.getlist('quantity[]')
        prices       = request.POST.getlist('sale_price[]')
        custom_names = request.POST.getlist('custom_name[]')
        is_manuals   = request.POST.getlist('is_manual[]')

        for i in range(len(quantities)):
            qty   = Decimal(str(quantities[i] or 0))
            price = Decimal(str(prices[i] or 0))
            if qty <= 0:
                continue

            is_manual = is_manuals[i] == 'yes' if i < len(is_manuals) else False

            if is_manual:
                custom_name = custom_names[i] if i < len(custom_names) else ''
                SaleItem.objects.create(
                    sale                = sale,
                    product             = None,
                    custom_product_name = custom_name,
                    quantity            = qty,
                    sale_price          = price,
                    purchase_price      = 0,
                )
            else:
                pid = product_ids[i] if i < len(product_ids) else ''
                if not pid:
                    continue
                product = Product.objects.filter(pk=pid).first()
                if not product:
                    continue

                if product.stock < qty:
                    messages.error(request, f'Insufficient stock for {product.name}.')
                    sale.delete()
                    return redirect('sale_add')

                SaleItem.objects.create(
                    sale           = sale,
                    product        = product,
                    quantity       = qty,
                    sale_price     = price,
                    purchase_price = product.purchase_price,
                )
                product.stock -= qty
                product.save()

        messages.success(request, f'Sale #{invoice_number} recorded successfully.')
        return redirect('sale_detail', pk=sale.pk)

    return render(request, 'sales/sale_add.html', {
        'products':  products,
        'customers': customers,
        'today':     timezone.now().date(),
    })


@login_required
def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'sales/sale_detail.html', {'sale': sale})


@login_required
def sale_edit(request, pk):
    sale      = get_object_or_404(Sale, pk=pk)
    products  = Product.objects.filter(is_active=True)
    customers = Customer.objects.all()

    if request.method == 'POST':
        for item in sale.items.all():
            if item.product:
                item.product.stock += item.quantity
                item.product.save()
        sale.items.all().delete()

        customer_id    = request.POST.get('customer') or None
        payment_method = request.POST.get('payment_method')
        discount       = round(Decimal(str(request.POST.get('discount') or 0)), 2)
        advance        = Decimal(str(request.POST.get('advance_payment') or 0))
        notes          = request.POST.get('notes') or None

        customer_name_input = request.POST.get('customer_name_input', '').strip()
        if not customer_id and customer_name_input:
            customer_obj, _ = Customer.objects.get_or_create(name=customer_name_input)
            customer_id = customer_obj.pk

        sale.customer_id     = customer_id
        sale.payment_method  = payment_method
        sale.discount        = discount
        sale.advance_payment = advance
        sale.notes           = notes
        sale.save()

        product_ids  = request.POST.getlist('product_id[]')
        quantities   = request.POST.getlist('quantity[]')
        prices       = request.POST.getlist('sale_price[]')
        custom_names = request.POST.getlist('custom_name[]')
        is_manuals   = request.POST.getlist('is_manual[]')

        for i in range(len(quantities)):
            qty   = Decimal(str(quantities[i] or 0))
            price = Decimal(str(prices[i] or 0))
            if qty <= 0:
                continue

            is_manual = is_manuals[i] == 'yes' if i < len(is_manuals) else False

            if is_manual:
                custom_name = custom_names[i] if i < len(custom_names) else ''
                SaleItem.objects.create(
                    sale                = sale,
                    product             = None,
                    custom_product_name = custom_name,
                    quantity            = qty,
                    sale_price          = price,
                    purchase_price      = 0,
                )
            else:
                pid = product_ids[i] if i < len(product_ids) else ''
                if not pid:
                    continue
                product = Product.objects.filter(pk=pid).first()
                if not product:
                    continue

                if product.stock < qty:
                    messages.error(request, f'Insufficient stock for {product.name}.')
                    return redirect('sale_edit', pk=pk)

                SaleItem.objects.create(
                    sale           = sale,
                    product        = product,
                    quantity       = qty,
                    sale_price     = price,
                    purchase_price = product.purchase_price,
                )
                product.stock -= qty
                product.save()

        messages.success(request, f'Sale #{sale.invoice_number} updated successfully.')
        return redirect('sale_detail', pk=sale.pk)

    return render(request, 'sales/sale_edit.html', {
        'sale':      sale,
        'products':  products,
        'customers': customers,
    })


@login_required
def sale_delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    for item in sale.items.all():
        if item.product:
            item.product.stock += item.quantity
            item.product.save()
    sale.delete()
    messages.success(request, 'Sale deleted successfully.')
    return redirect('sale_list')


@login_required
def customer_search(request):
    from django.http import JsonResponse
    q         = request.GET.get('q', '')
    customers = Customer.objects.filter(name__icontains=q)[:10]
    data      = [{'id': c.pk, 'name': c.name, 'phone': c.phone or ''} for c in customers]
    return JsonResponse({'customers': data})


@login_required
def sale_return_create(request, sale_id):
    sale     = get_object_or_404(Sale, pk=sale_id)
    products = Product.objects.filter(is_active=True)

    if request.method == 'POST':
        return_type = request.POST.get('return_type')
        notes       = request.POST.get('notes', '')

        ret_product_ids = request.POST.getlist('ret_product_id[]')
        ret_customs     = request.POST.getlist('ret_custom_name[]')
        ret_is_manuals  = request.POST.getlist('ret_is_manual[]')
        ret_qtys        = request.POST.getlist('ret_quantity[]')
        ret_prices      = request.POST.getlist('ret_price[]')

        exc_product_ids = request.POST.getlist('exc_product_id[]')
        exc_customs     = request.POST.getlist('exc_custom_name[]')
        exc_is_manuals  = request.POST.getlist('exc_is_manual[]')
        exc_qtys        = request.POST.getlist('exc_quantity[]')
        exc_prices      = request.POST.getlist('exc_price[]')

        refund_amount   = Decimal('0')
        exchange_amount = Decimal('0')

        sale_return = SaleReturn.objects.create(
            sale        = sale,
            return_type = return_type,
            notes       = notes,
            created_by  = request.user
        )

        for i in range(len(ret_qtys)):
            qty   = Decimal(str(ret_qtys[i] or 0))
            price = Decimal(str(ret_prices[i] or 0))
            if qty <= 0:
                continue
            is_manual = ret_is_manuals[i] == 'yes'
            product   = None
            name      = ''
            if is_manual:
                name = ret_customs[i]
            else:
                pid = ret_product_ids[i]
                if pid:
                    product = Product.objects.filter(pk=pid).first()
                    if product:
                        name = product.name
                        product.stock += qty
                        product.save()

            SaleReturnItem.objects.create(
                sale_return = sale_return,
                product     = product,
                custom_name = name,
                quantity    = qty,
                price       = price,
                total       = qty * price
            )
            refund_amount += qty * price

        if return_type == 'exchange':
            for i in range(len(exc_qtys)):
                qty   = Decimal(str(exc_qtys[i] or 0))
                price = Decimal(str(exc_prices[i] or 0))
                if qty <= 0:
                    continue
                is_manual = exc_is_manuals[i] == 'yes'
                product   = None
                name      = ''
                if is_manual:
                    name = exc_customs[i]
                else:
                    pid = exc_product_ids[i]
                    if pid:
                        product = Product.objects.filter(pk=pid).first()
                        if product:
                            name = product.name
                            product.stock -= qty
                            product.save()

                SaleExchangeItem.objects.create(
                    sale_return = sale_return,
                    product     = product,
                    custom_name = name,
                    quantity    = qty,
                    price       = price,
                    total       = qty * price
                )
                exchange_amount += qty * price

        net_balance = exchange_amount - refund_amount

        sale_return.refund_amount   = refund_amount
        sale_return.exchange_amount = exchange_amount
        sale_return.net_balance     = net_balance
        sale_return.save()

        messages.success(request, f'Return #RTN-{sale_return.pk} processed successfully.')
        return redirect('sale_return_invoice', pk=sale_return.pk)

    return render(request, 'sales/sale_return_form.html', {
        'sale':     sale,
        'products': products,
    })


@login_required
def sale_return_invoice(request, pk):
    sale_return = get_object_or_404(SaleReturn, pk=pk)
    return render(request, 'sales/sale_return_invoice.html', {
        'r': sale_return,
    })


@login_required
def sale_return_list(request):
    returns = SaleReturn.objects.select_related(
        'sale', 'sale__customer'
    ).order_by('-date')
    return render(request, 'sales/sale_return_list.html', {
        'returns': returns,
    })
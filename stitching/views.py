from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from decimal import Decimal
from .models import StitchingOrder
from products.models import Product
from customers.models import Customer

STANDARD_SIZES = {
    '20': {'shirt_length': '22', 'shoulder': '10', 'chest': '22', 'waist': '20', 'sleeve_length': '10', 'collar': '10', 'shalwar_length': '20', 'shalwar_waist': '18', 'hip': '22', 'bottom_width': '10'},
    '22': {'shirt_length': '24', 'shoulder': '11', 'chest': '24', 'waist': '22', 'sleeve_length': '11', 'collar': '11', 'shalwar_length': '22', 'shalwar_waist': '20', 'hip': '24', 'bottom_width': '11'},
    '24': {'shirt_length': '26', 'shoulder': '12', 'chest': '26', 'waist': '24', 'sleeve_length': '12', 'collar': '12', 'shalwar_length': '24', 'shalwar_waist': '22', 'hip': '26', 'bottom_width': '12'},
    '26': {'shirt_length': '28', 'shoulder': '13', 'chest': '28', 'waist': '26', 'sleeve_length': '13', 'collar': '13', 'shalwar_length': '26', 'shalwar_waist': '24', 'hip': '28', 'bottom_width': '13'},
    '28': {'shirt_length': '30', 'shoulder': '14', 'chest': '30', 'waist': '28', 'sleeve_length': '14', 'collar': '14', 'shalwar_length': '28', 'shalwar_waist': '26', 'hip': '30', 'bottom_width': '14'},
    '30': {'shirt_length': '32', 'shoulder': '15', 'chest': '32', 'waist': '30', 'sleeve_length': '15', 'collar': '15', 'shalwar_length': '30', 'shalwar_waist': '28', 'hip': '32', 'bottom_width': '15'},
    '32': {'shirt_length': '38', 'shoulder': '15', 'chest': '34', 'waist': '32', 'sleeve_length': '23', 'collar': '13', 'shalwar_length': '38', 'shalwar_waist': '32', 'hip': '34', 'bottom_width': '14'},
    '34': {'shirt_length': '40', 'shoulder': '16', 'chest': '36', 'waist': '34', 'sleeve_length': '24', 'collar': '14', 'shalwar_length': '40', 'shalwar_waist': '34', 'hip': '36', 'bottom_width': '15'},
    '36': {'shirt_length': '42', 'shoulder': '17', 'chest': '38', 'waist': '36', 'sleeve_length': '24.5', 'collar': '14.5', 'shalwar_length': '42', 'shalwar_waist': '36', 'hip': '38', 'bottom_width': '15'},
    '38': {'shirt_length': '44', 'shoulder': '17.5', 'chest': '40', 'waist': '38', 'sleeve_length': '25', 'collar': '15', 'shalwar_length': '44', 'shalwar_waist': '38', 'hip': '40', 'bottom_width': '16'},
    '40': {'shirt_length': '46', 'shoulder': '18', 'chest': '42', 'waist': '40', 'sleeve_length': '25.5', 'collar': '15.5', 'shalwar_length': '46', 'shalwar_waist': '40', 'hip': '42', 'bottom_width': '16'},
    '42': {'shirt_length': '48', 'shoulder': '18.5', 'chest': '44', 'waist': '42', 'sleeve_length': '26', 'collar': '16', 'shalwar_length': '48', 'shalwar_waist': '42', 'hip': '44', 'bottom_width': '17'},
    '44': {'shirt_length': '50', 'shoulder': '19', 'chest': '46', 'waist': '44', 'sleeve_length': '26.5', 'collar': '16.5', 'shalwar_length': '50', 'shalwar_waist': '44', 'hip': '46', 'bottom_width': '17'},
    '46': {'shirt_length': '52', 'shoulder': '19.5', 'chest': '48', 'waist': '46', 'sleeve_length': '27', 'collar': '17', 'shalwar_length': '52', 'shalwar_waist': '46', 'hip': '48', 'bottom_width': '18'},
}


@login_required
def get_size_measurements(request):
    size = request.GET.get('size')
    customer_id = request.GET.get('customer_id')
    data = {}
    if size and size in STANDARD_SIZES:
        data = STANDARD_SIZES[size].copy()
    if customer_id:
        try:
            customer = Customer.objects.get(pk=customer_id)
            if customer.saved_size == size or size == 'custom':
                if customer.saved_shirt_length: data['shirt_length'] = customer.saved_shirt_length
                if customer.saved_shoulder: data['shoulder'] = customer.saved_shoulder
                if customer.saved_chest: data['chest'] = customer.saved_chest
                if customer.saved_waist: data['waist'] = customer.saved_waist
                if customer.saved_sleeve_length: data['sleeve_length'] = customer.saved_sleeve_length
                if customer.saved_collar: data['collar'] = customer.saved_collar
                if customer.saved_shalwar_length: data['shalwar_length'] = customer.saved_shalwar_length
                if customer.saved_shalwar_waist: data['shalwar_waist'] = customer.saved_shalwar_waist
                if customer.saved_hip: data['hip'] = customer.saved_hip
                if customer.saved_bottom_width: data['bottom_width'] = customer.saved_bottom_width
                if customer.saved_extra_measurements: data['extra_measurements'] = customer.saved_extra_measurements
        except Customer.DoesNotExist:
            pass
    return JsonResponse(data)


@login_required
def get_customer_measurements(request):
    customer_id = request.GET.get('customer_id')
    if customer_id:
        try:
            customer = Customer.objects.get(pk=customer_id)
            data = {
                'name': customer.name,
                'phone': customer.phone or '',
                'size': customer.saved_size or '',
                'shirt_length': customer.saved_shirt_length or '',
                'shoulder': customer.saved_shoulder or '',
                'chest': customer.saved_chest or '',
                'waist': customer.saved_waist or '',
                'sleeve_length': customer.saved_sleeve_length or '',
                'collar': customer.saved_collar or '',
                'shalwar_length': customer.saved_shalwar_length or '',
                'shalwar_waist': customer.saved_shalwar_waist or '',
                'hip': customer.saved_hip or '',
                'bottom_width': customer.saved_bottom_width or '',
                'extra_measurements': customer.saved_extra_measurements or '',
            }
            return JsonResponse(data)
        except Customer.DoesNotExist:
            pass
    return JsonResponse({})


@login_required
def stitching_list(request):
    search = request.GET.get('search', '')
    orders = StitchingOrder.objects.all().order_by('-created_at')
    if search:
        orders = orders.filter(customer_name__icontains=search) | orders.filter(customer_phone__icontains=search)
    pending     = StitchingOrder.objects.filter(status='pending').count()
    in_progress = StitchingOrder.objects.filter(status='in_progress').count()
    completed   = StitchingOrder.objects.filter(status='completed').count()
    delivered   = StitchingOrder.objects.filter(status='delivered').count()
    return render(request, 'stitching/stitching_list.html', {
        'orders':      orders,
        'pending':     pending,
        'in_progress': in_progress,
        'completed':   completed,
        'delivered':   delivered,
        'search':      search,
    })


@login_required
def stitching_detail(request, pk):
    order = get_object_or_404(StitchingOrder, pk=pk)
    return render(request, 'stitching/stitching_detail.html', {'order': order})


@login_required
def stitching_add(request):
    products  = Product.objects.filter(is_active=True)
    customers = Customer.objects.all().order_by('name')
    if request.method == 'POST':
        customer_id = request.POST.get('customer') or None
        fabric_id   = request.POST.get('fabric') or None
        fabric_qty  = Decimal(str(request.POST.get('fabric_quantity') or 0))
        if fabric_id:
            fabric = Product.objects.get(pk=fabric_id)
            if fabric.stock < fabric_qty:
                messages.error(request, f'Insufficient fabric stock. Available: {fabric.stock}')
                return render(request, 'stitching/stitching_add.html', {'products': products, 'customers': customers})
            fabric.stock -= fabric_qty
            fabric.save()
        order = StitchingOrder.objects.create(
            customer_id     = customer_id,
            customer_name   = request.POST.get('customer_name'),
            customer_phone  = request.POST.get('customer_phone') or None,
            code_number     = request.POST.get('code_number') or None,
            fabric_id       = fabric_id,
            fabric_quantity = fabric_qty,
            stitching_cost  = Decimal(str(request.POST.get('stitching_cost') or 0)),
            advance_payment = Decimal(str(request.POST.get('advance_payment') or 0)),
            delivery_date   = request.POST.get('delivery_date') or None,
            status          = request.POST.get('status'),
            size            = request.POST.get('size') or None,
            shirt_length    = request.POST.get('shirt_length') or None,
            shoulder        = request.POST.get('shoulder') or None,
            chest           = request.POST.get('chest') or None,
            waist           = request.POST.get('waist') or None,
            sleeve_length   = request.POST.get('sleeve_length') or None,
            collar          = request.POST.get('collar') or None,
            shalwar_length  = request.POST.get('shalwar_length') or None,
            shalwar_waist   = request.POST.get('shalwar_waist') or None,
            hip             = request.POST.get('hip') or None,
            bottom_width    = request.POST.get('bottom_width') or None,
            extra_measurements = request.POST.get('extra_measurements') or None,
            notes           = request.POST.get('notes') or None,
        )
        if customer_id:
            customer = Customer.objects.get(pk=customer_id)
            customer.saved_size             = request.POST.get('size') or None
            customer.saved_shirt_length     = request.POST.get('shirt_length') or None
            customer.saved_shoulder         = request.POST.get('shoulder') or None
            customer.saved_chest            = request.POST.get('chest') or None
            customer.saved_waist            = request.POST.get('waist') or None
            customer.saved_sleeve_length    = request.POST.get('sleeve_length') or None
            customer.saved_collar           = request.POST.get('collar') or None
            customer.saved_shalwar_length   = request.POST.get('shalwar_length') or None
            customer.saved_shalwar_waist    = request.POST.get('shalwar_waist') or None
            customer.saved_hip              = request.POST.get('hip') or None
            customer.saved_bottom_width     = request.POST.get('bottom_width') or None
            customer.saved_extra_measurements = request.POST.get('extra_measurements') or None
            customer.save()
        messages.success(request, 'Stitching order added successfully.')
        return redirect('stitching_detail', pk=order.pk)
    return render(request, 'stitching/stitching_add.html', {'products': products, 'customers': customers})


@login_required
def stitching_edit(request, pk):
    order     = get_object_or_404(StitchingOrder, pk=pk)
    products  = Product.objects.filter(is_active=True)
    customers = Customer.objects.all().order_by('name')
    if request.method == 'POST':
        customer_id         = request.POST.get('customer') or None
        order.customer_id   = customer_id
        order.customer_name = request.POST.get('customer_name')
        order.customer_phone = request.POST.get('customer_phone') or None
        order.code_number   = request.POST.get('code_number') or None
        order.delivery_date = request.POST.get('delivery_date') or None
        order.status        = request.POST.get('status')
        order.stitching_cost  = Decimal(str(request.POST.get('stitching_cost') or 0))
        order.advance_payment = Decimal(str(request.POST.get('advance_payment') or 0))
        order.size          = request.POST.get('size') or None
        order.shirt_length  = request.POST.get('shirt_length') or None
        order.shoulder      = request.POST.get('shoulder') or None
        order.chest         = request.POST.get('chest') or None
        order.waist         = request.POST.get('waist') or None
        order.sleeve_length = request.POST.get('sleeve_length') or None
        order.collar        = request.POST.get('collar') or None
        order.shalwar_length = request.POST.get('shalwar_length') or None
        order.shalwar_waist  = request.POST.get('shalwar_waist') or None
        order.hip            = request.POST.get('hip') or None
        order.bottom_width   = request.POST.get('bottom_width') or None
        order.extra_measurements = request.POST.get('extra_measurements') or None
        order.notes          = request.POST.get('notes') or None
        order.save()
        if customer_id:
            customer = Customer.objects.get(pk=customer_id)
            customer.saved_size             = request.POST.get('size') or None
            customer.saved_shirt_length     = request.POST.get('shirt_length') or None
            customer.saved_shoulder         = request.POST.get('shoulder') or None
            customer.saved_chest            = request.POST.get('chest') or None
            customer.saved_waist            = request.POST.get('waist') or None
            customer.saved_sleeve_length    = request.POST.get('sleeve_length') or None
            customer.saved_collar           = request.POST.get('collar') or None
            customer.saved_shalwar_length   = request.POST.get('shalwar_length') or None
            customer.saved_shalwar_waist    = request.POST.get('shalwar_waist') or None
            customer.saved_hip              = request.POST.get('hip') or None
            customer.saved_bottom_width     = request.POST.get('bottom_width') or None
            customer.saved_extra_measurements = request.POST.get('extra_measurements') or None
            customer.save()
        messages.success(request, 'Stitching order updated successfully.')
        return redirect('stitching_detail', pk=order.pk)
    return render(request, 'stitching/stitching_edit.html', {
        'order':     order,
        'products':  products,
        'customers': customers,
    })


@login_required
def stitching_delete(request, pk):
    order = get_object_or_404(StitchingOrder, pk=pk)
    if order.fabric and order.fabric_quantity:
        order.fabric.stock += order.fabric_quantity
        order.fabric.save()
    order.delete()
    messages.success(request, 'Stitching order deleted successfully.')
    return redirect('stitching_list')
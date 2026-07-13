from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta


@login_required
def dashboard(request):
    today = timezone.now().date()
    month_start = today.replace(day=1)
    last_30 = today - timedelta(days=30)

    # Import models
    from sales.models import Sale
    from purchases.models import PurchaseInvoice
    from expenses.models import Expense
    from products.models import Product
    from customers.models import Customer
    from stitching.models import StitchingOrder

    # Today sales
    today_sales = Sale.objects.filter(sale_date__date=today)
    today_revenue = sum(s.net_total for s in today_sales)
    today_orders = today_sales.count()

    # Last 30 days
    last30_sales = Sale.objects.filter(sale_date__date__gte=last_30)
    last30_revenue = sum(s.net_total for s in last30_sales)
    last30_orders = last30_sales.count()

    # This month purchases
    monthly_purchases = PurchaseInvoice.objects.filter(invoice_date__gte=month_start)
    monthly_purchase_total = sum(p.net_total for p in monthly_purchases)
    monthly_purchase_count = monthly_purchases.count()

    # Low stock alerts
    low_stock = Product.objects.filter(stock__lte=5, is_active=True).count()

    # Stitching orders
    pending_stitching = StitchingOrder.objects.filter(status='pending').count()

    # Today expenses
    today_expenses = Expense.objects.filter(date=today)
    today_expense_total = sum(e.amount for e in today_expenses)

    # Total products and customers
    total_products = Product.objects.filter(is_active=True).count()
    total_customers = Customer.objects.count()

    # Recent sales
    recent_sales = Sale.objects.all().order_by('-sale_date')[:5]

    # Low stock products
    low_stock_products = Product.objects.filter(
        stock__lte=5,
        is_active=True
    ).order_by('stock')[:5]

    # Last 30 days chart data
    chart_labels = []
    chart_data = []
    for i in range(29, -1, -1):
        day = today - timedelta(days=i)
        day_sales = Sale.objects.filter(sale_date__date=day)
        day_revenue = float(sum(s.net_total for s in day_sales))
        chart_labels.append(day.strftime('%d %b'))
        chart_data.append(day_revenue)

    # Stitching status for chart
    stitching_pending = StitchingOrder.objects.filter(status='pending').count()
    stitching_progress = StitchingOrder.objects.filter(status='in_progress').count()
    stitching_completed = StitchingOrder.objects.filter(status='completed').count()

    return render(request, 'dashboard/dashboard.html', {
        'today_revenue': today_revenue,
        'today_orders': today_orders,
        'last30_revenue': last30_revenue,
        'last30_orders': last30_orders,
        'monthly_purchase_total': monthly_purchase_total,
        'monthly_purchase_count': monthly_purchase_count,
        'low_stock': low_stock,
        'pending_stitching': pending_stitching,
        'today_expense_total': today_expense_total,
        'total_products': total_products,
        'total_customers': total_customers,
        'recent_sales': recent_sales,
        'low_stock_products': low_stock_products,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'stitching_pending': stitching_pending,
        'stitching_progress': stitching_progress,
        'stitching_completed': stitching_completed,
    })
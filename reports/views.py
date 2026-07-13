from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse
from datetime import date, timedelta
import csv

from sales.models import Sale, SaleItem
from purchases.models import PurchaseInvoice
from expenses.models import Expense
from products.models import Product


@login_required
def reports_home(request):
    today = timezone.now().date()
    month_start = today.replace(day=1)

    # Today Sales stats
    today_sales = Sale.objects.filter(sale_date__date=today)
    today_revenue = sum(s.net_total for s in today_sales)
    today_profit = sum(s.total_profit for s in today_sales)
    today_discount = sum(s.discount_amount for s in today_sales)
    today_sales_count = today_sales.count()

    # Monthly Sales stats
    monthly_sales = Sale.objects.filter(sale_date__date__gte=month_start)
    monthly_revenue = sum(s.net_total for s in monthly_sales)
    monthly_profit = sum(s.total_profit for s in monthly_sales)
    monthly_discount = sum(s.discount_amount for s in monthly_sales)
    monthly_sales_count = monthly_sales.count()

    # Purchase stats
    monthly_purchases = PurchaseInvoice.objects.filter(invoice_date__gte=month_start)
    monthly_purchase_total = sum(p.net_total for p in monthly_purchases)

    # Expense stats
    today_expenses = Expense.objects.filter(date=today)
    today_expense_total = sum(e.amount for e in today_expenses)
    monthly_expenses = Expense.objects.filter(date__gte=month_start)
    monthly_expense_total = sum(e.amount for e in monthly_expenses)

    # Net profit
    net_profit = monthly_profit - monthly_expense_total

    return render(request, 'reports/reports_home.html', {
        'today_revenue': today_revenue,
        'today_profit': today_profit,
        'today_discount': today_discount,
        'today_sales_count': today_sales_count,
        'today_expense_total': today_expense_total,
        'monthly_revenue': monthly_revenue,
        'monthly_profit': monthly_profit,
        'monthly_discount': monthly_discount,
        'monthly_sales_count': monthly_sales_count,
        'monthly_purchase_total': monthly_purchase_total,
        'monthly_expense_total': monthly_expense_total,
        'net_profit': net_profit,
    })


@login_required
def sales_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    sales = Sale.objects.all().order_by('-sale_date')

    if start_date:
        sales = sales.filter(sale_date__date__gte=start_date)
    if end_date:
        sales = sales.filter(sale_date__date__lte=end_date)

    total_revenue = sum(s.net_total for s in sales)
    total_profit = sum(s.total_profit for s in sales)

    return render(request, 'reports/sales_report.html', {
        'sales': sales,
        'total_revenue': total_revenue,
        'total_profit': total_profit,
        'start_date': start_date,
        'end_date': end_date,
    })


@login_required
def purchases_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    invoices = PurchaseInvoice.objects.all().order_by('-invoice_date')

    if start_date:
        invoices = invoices.filter(invoice_date__gte=start_date)
    if end_date:
        invoices = invoices.filter(invoice_date__lte=end_date)

    total = sum(inv.net_total for inv in invoices)
    total_paid = sum(inv.paid_amount for inv in invoices)
    total_balance = total - total_paid

    return render(request, 'reports/purchases_report.html', {
        'invoices': invoices,
        'total': total,
        'total_paid': total_paid,
        'total_balance': total_balance,
        'start_date': start_date,
        'end_date': end_date,
    })


@login_required
def expenses_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    expenses = Expense.objects.all().order_by('-date')

    if start_date:
        expenses = expenses.filter(date__gte=start_date)
    if end_date:
        expenses = expenses.filter(date__lte=end_date)

    total = sum(e.amount for e in expenses)

    return render(request, 'reports/expenses_report.html', {
        'expenses': expenses,
        'total': total,
        'start_date': start_date,
        'end_date': end_date,
    })


@login_required
def profit_loss_report(request):
    today = timezone.now().date()
    month_start = today.replace(day=1)

    start_date = request.GET.get('start_date', str(month_start))
    end_date = request.GET.get('end_date', str(today))

    sales = Sale.objects.filter(sale_date__date__gte=start_date, sale_date__date__lte=end_date)
    expenses = Expense.objects.filter(date__gte=start_date, date__lte=end_date)

    total_revenue = sum(s.net_total for s in sales)
    total_profit = sum(s.total_profit for s in sales)
    total_expenses = sum(e.amount for e in expenses)
    net_profit = total_profit - total_expenses

    return render(request, 'reports/profit_loss_report.html', {
        'total_revenue': total_revenue,
        'total_profit': total_profit,
        'total_expenses': total_expenses,
        'net_profit': net_profit,
        'start_date': start_date,
        'end_date': end_date,
    })


@login_required
def inventory_report(request):
    products = Product.objects.all().order_by('name')
    low_stock = products.filter(stock__lte=5)
    total_value = sum(p.stock * p.purchase_price for p in products)

    return render(request, 'reports/inventory_report.html', {
        'products': products,
        'low_stock': low_stock,
        'total_value': total_value,
    })


@login_required
def export_sales_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Invoice No', 'Customer', 'Date', 'Payment', 'Total', 'Profit'])
    for sale in Sale.objects.all().order_by('-sale_date'):
        writer.writerow([
            sale.invoice_number,
            sale.customer.name if sale.customer else 'Walk-in',
            sale.sale_date.strftime('%d %b %Y'),
            sale.get_payment_method_display(),
            sale.net_total,
            sale.total_profit,
        ])
    return response


@login_required
def export_purchases_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="purchases_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Invoice No', 'Supplier', 'Date', 'Total', 'Paid', 'Balance', 'Status'])
    for inv in PurchaseInvoice.objects.all().order_by('-invoice_date'):
        writer.writerow([
            inv.invoice_number,
            inv.supplier.name,
            inv.invoice_date.strftime('%d %b %Y'),
            inv.net_total,
            inv.paid_amount,
            inv.balance,
            inv.status,
        ])
    return response


@login_required
def export_expenses_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Title', 'Category', 'Amount', 'Date', 'Notes'])
    for exp in Expense.objects.all().order_by('-date'):
        writer.writerow([
            exp.title,
            exp.category.name if exp.category else '-',
            exp.amount,
            exp.date.strftime('%d %b %Y'),
            exp.notes or '-',
        ])
    return response
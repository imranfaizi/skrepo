from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Expense, ExpenseCategory

ADMIN_PASSWORD = 'boutique123'

@login_required
def expense_list(request):
    search = request.GET.get('search', '')
    expenses = Expense.objects.all().order_by('-date')
    if search:
        expenses = expenses.filter(title__icontains=search) | expenses.filter(category__name__icontains=search)
    total = sum(exp.amount for exp in expenses)
    today = timezone.now().date()
    today_total = sum(exp.amount for exp in Expense.objects.filter(date=today))
    return render(request, 'expenses/expense_list.html', {
        'expenses': expenses,
        'total': total,
        'today_total': today_total,
        'search': search,
    })

@login_required
def expense_add(request):
    categories = ExpenseCategory.objects.all()
    if request.method == 'POST':
        Expense.objects.create(
            category_id=request.POST.get('category') or None,
            title=request.POST.get('title'),
            amount=request.POST.get('amount'),
            date=request.POST.get('date'),
            notes=request.POST.get('notes') or None,
        )
        messages.success(request, 'Expense added successfully.')
        return redirect('expense_list')
    return render(request, 'expenses/expense_add.html', {
        'categories': categories,
        'today': timezone.now().date(),
    })

@login_required
def expense_edit(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    categories = ExpenseCategory.objects.all()
    if request.method == 'POST':
        password = request.POST.get('edit_password', '')
        if password != ADMIN_PASSWORD:
            messages.error(request, 'Incorrect password! Changes not saved.')
            return render(request, 'expenses/expense_edit.html', {'expense': expense, 'categories': categories})
        expense.category_id = request.POST.get('category') or None
        expense.title = request.POST.get('title')
        expense.amount = request.POST.get('amount')
        expense.date = request.POST.get('date')
        expense.notes = request.POST.get('notes') or None
        expense.save()
        messages.success(request, 'Expense updated successfully.')
        return redirect('expense_list')
    return render(request, 'expenses/expense_edit.html', {
        'expense': expense,
        'categories': categories,
    })

@login_required
def expense_delete(request, pk):
    if request.method == 'POST':
        password = request.POST.get('delete_password', '')
        if password != ADMIN_PASSWORD:
            messages.error(request, 'Incorrect password! Expense not deleted.')
            return redirect('expense_list')
        expense = get_object_or_404(Expense, pk=pk)
        expense.delete()
        messages.success(request, 'Expense deleted successfully.')
    return redirect('expense_list')

@login_required
def category_list(request):
    categories = ExpenseCategory.objects.all()
    return render(request, 'expenses/category_list.html', {'categories': categories})

@login_required
def category_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            ExpenseCategory.objects.create(name=name)
            messages.success(request, 'Category added successfully.')
            return redirect('expense_category_list')
    return render(request, 'expenses/category_add.html')

@login_required
def category_delete(request, pk):
    if request.method == 'POST':
        password = request.POST.get('delete_password', '')
        if password != ADMIN_PASSWORD:
            messages.error(request, 'Incorrect password!')
            return redirect('expense_category_list')
        category = get_object_or_404(ExpenseCategory, pk=pk)
        category.delete()
        messages.success(request, 'Category deleted successfully.')
    return redirect('expense_category_list')
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from .models import Expense
from expenses.forms import ExpenseForm,EmailLoginForm,RegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Sum

# Imports for time
from datetime import date
from django.utils import timezone

# Create your views here.

def helllo(response):
    return HttpResponse("Hello, world!")

@login_required
def expense_list(request):
    expense=Expense.objects.filter(user=request.user)
    
    category=request.GET.get('category')
    start_date=request.GET.get('start_date')
    end_date=request.GET.get('end_date')
    if category:
        expense=expense.filter(category=category).order_by('-date')
    if start_date:
        expense=expense.filter(date__gte=start_date)
    if end_date:
        expense=expense.filter(date__lte=end_date)
    expense=expense.order_by('-date')

    total_expenses=expense.aggregate(total=Sum('amount'))['total'] or 0
    context={'expense':expense,'total_expenses':total_expenses,'category':category,'start_date': start_date,
        'end_date': end_date,}
    return render(request,'expenses/expense.html',context)


@login_required
def add_expense(request):
    if request.method=="POST":
        form=ExpenseForm(request.POST)
        if form.is_valid():
            expense=form.save(commit=False)
            expense.user=request.user
            expense.save()
            messages.success(request,"Successfully added expense")
            return redirect('expense_list')
    else:
        form=ExpenseForm()
    return render(request,'expenses/add_expense.html',{'form':form})


def email_login(request):
    if request.method == "POST":
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            # Entire validation process of input field happens in this is_valid() function
            # Check for data type of input field and structure of field if used for eg whether email contains . or @ 
            login(request, form.user)
            return redirect('expense_list')
        
    else:
        form = EmailLoginForm()
    return render(request,'expenses/login.html',{'form':form})


def register(request):
    if request.method == "POST":
        form=RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('expense_list')
    else:
        form=RegistrationForm()
    return render(request,'expenses/register.html',{'form':form})

@login_required
def dashboard(request):
    today = date.today()
    user_expense=Expense.objects.filter(user=request.user)
    monthly_total=user_expense.filter(date__year=today.year,date__month=today.month).aggregate(total=Sum('amount'))['total'] or 0
    total_expense=user_expense.aggregate(total=Sum('amount'))['total'] or 0
    total_count=user_expense.count()
    month_count=user_expense.filter(date__year=today.year,date__month=today.month).count()
    recent_expenses=user_expense.order_by('-date')[:5]
    category_summary = user_expense.values('category').annotate(total=Sum('amount'))
    # In django user.objects.constraint gives query set as: [
    # {"category": "Food", "amount": 50},
    # {"category": "Food", "amount": 20},
    # ]
    # And when you do this user_expense.values('category') it returns a dictionary of distinct items
    # [
#     {"category": "Food"},
#     {"category": "Food"},
#     {"category": "Travel"},
# ]
    
    # You may think what annote does its just aggregation function done to every field
    # This performs an aggregation — it adds a computed field to each group from values(). In this case, it’s summing up the amount field for each group.

    context={
        "monthly_total": monthly_total,
        "total_expense": total_expense,
        "total_count": total_count,
        "month_count": month_count,
        "recent_expenses": recent_expenses,
        "category_summary": category_summary
    }

    return render(request,'expenses/dashboard.html',context)

def edit(request,pk):
    instance=get_object_or_404(Expense,pk=pk,user=request.user)
    if request.method=="POST":
        form=ExpenseForm(request.POST,instance=instance)
        if form.is_valid():
            expense=form.save(commit=False)
            expense.user=request.user
            expense.save()
            return redirect('expense_list')
    else:
        form=ExpenseForm(instance=instance)
    
    return render(request,'expenses/edit_expense.html',{'form':form})




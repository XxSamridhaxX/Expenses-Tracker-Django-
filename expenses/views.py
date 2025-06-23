from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from .models import Expense
from expenses.forms import ExpenseForm,EmailLoginForm,RegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Sum
from django.contrib import messages
from django.db.models.functions import TruncMonth

# Imports for time
from datetime import date
from django.utils import timezone

# Create your views here.

def helllo(response):
     return HttpResponse("Hello, world!")


# Paginator breaks the content into pages
from django.core.paginator import Paginator

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

    p= Paginator(expense,10)
    # Yo bhaneko Paginator object ho esma 2 ota parameter huncha query_list ra number of item in page. Esle item lai kasari page ma chuttaune calculate garcha

    page_number= request.GET.get('page')
    # link ma like /page=2 bhanera aucha hami jun page ma cham like next thichda pani link ma ta yei aucha ni even tho purai page load na bhaye ni.

    page_obj=p.get_page(page_number)
    # Esle chai hamlai tyo jun page ma cha tyo page ma chaiyeko objects or items haru dincha which can be displayed
    total_expenses=expense.aggregate(total=Sum('amount'))['total'] or 0
    context={'expense':expense,'total_expenses':total_expenses,'category':category,'start_date': start_date,
        'end_date': end_date,'page_obj':page_obj}
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
    # Category wise data
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
        # Monthly totals



  # Monthly totals for bar chart
    monthly_data = (
        user_expense
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )
    month_labels = [item['month'].strftime('%B') for item in monthly_data]
    month_totals = [item['total'] for item in monthly_data]


    # Category-wise totals for donut chart (this month only)
    this_month_categories = (
        user_expense
        .filter(date__year=today.year, date__month=today.month)
        .values('category')
        .annotate(total=Sum('amount'))
    )
    category_labels = [item['category'] for item in this_month_categories]
    category_totals = [item['total'] for item in this_month_categories]
    context = {
    "monthly_total": monthly_total,
    "total_expense": total_expense,
    "total_count": total_count,
    "month_count": month_count,
    "recent_expenses": recent_expenses,
    "category_summary": category_summary,
    "monthly_data": monthly_data,
    "category_labels": category_labels,
    "category_totals":category_totals,
    "month_labels": month_labels,
    "month_totals": month_totals,
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
            messages.success(request,'Successfully saved changes')
            return redirect('expense_list')
    else:
        form=ExpenseForm(instance=instance)
    
    return render(request,'expenses/edit_expense.html',{'form':form})

def delete(request,pk):
    expense=get_object_or_404(Expense,pk=pk)
    expense.delete()
    messages.success(request,"Successfully deleted the expense item")
    return redirect('expense_list')



import csv
def export_csv(request):
    # To import all the data related to the user
    user_expense=Expense.objects.filter(user=request.user)
    if not user_expense.exists():
        messages.warning(request,"Don't have any data to export to CSV")
        return redirect('dashboard')

    response = HttpResponse(
        content_type="text/csv",
        headers= {"Content-Disposition": f'attachment; filename="{request.user}_expense_details.csv"'}
    )

    writer= csv.writer(response)
    writer.writerow(["title",'amount','category','date'])
    expense_fields = user_expense.values_list("title",'amount','category','date')
    for expense in expense_fields:
        writer.writerow(expense)
    return response

def export_filtered_csv(request):
    user_expense=Expense.objects.filter(user=request.user)

    category=request.GET.get('category')
    start_date=request.GET.get('start_date')
    end_date=request.GET.get('end_date')
    if category:
        user_expense=user_expense.filter(category=category)
    if start_date:
        user_expense=user_expense.filter(date__gte=start_date)   
    if end_date:
        user_expense=user_expense.filter(date__lte=end_date)   

    if not user_expense.exists():
        messages.warning(request, "No expenses found for the applied filters.")
        return redirect('expense_list')  # Use your actual view name here

    filename=f"{request.user.username}_{start_date}to{end_date}_{category}.csv"
    response= HttpResponse(content_type="text/csv",headers= {"Content-Disposition":f'attachment; filename="{filename}"'})
    writer=csv.writer(response)
    writer.writerow(['title','amount','category','date'])
    expense_field=user_expense.values_list('title','amount','category','date')
    for expense in expense_field:
        writer.writerow(expense)
    return response

# For the Changing of Password
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request, "Password changed successfully")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid password")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "expenses/change_password.html", {"form": form})
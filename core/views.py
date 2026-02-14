from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Sum
from django.utils import timezone
from .forms import ExpenseForm
from .models import Budget, Goal, Expense
from .forms import BudgetForm, GoalForm
from django.shortcuts import redirect




# ✅ LANDING PAGE
def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    return render(request, 'index.html')


# ✅ REGISTER
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('landing')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('landing')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()

        messages.success(request, "Account created! Please login.")
        return redirect('landing')

    return redirect('landing')


# ✅ LOGIN
@never_cache
def user_login(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')


# ✅ DASHBOARD (Now With Total Expense)
@login_required(login_url='login')
@never_cache
def dashboard(request):

    user_expenses = Expense.objects.filter(user=request.user)

    # 🔹 Total Expense
    total_expense = user_expenses.aggregate(
        Sum('amount')
    )['amount__sum'] or 0

    # 🔹 Total Number of Expenses
    expense_count = user_expenses.count()

    # 🔹 This Month Expense
    now = timezone.now()
    monthly_expense = user_expenses.filter(
        date__year=now.year,
        date__month=now.month
    ).aggregate(
        Sum('amount')
    )['amount__sum'] or 0

    # 🔹 Recent 5 Expenses
    recent_expenses = user_expenses.order_by('-date')[:5]

    context = {
        'total_expense': total_expense,
        'monthly_expense': monthly_expense,
        'expense_count': expense_count,
        'recent_expenses': recent_expenses
    }

    return render(request, 'dashboard.html', context)



# ✅ EXPENSE TRACKING VIEW
@login_required(login_url='login')
def expense_tracking(request):
    expenses = Expense.objects.filter(
        user=request.user
    ).order_by('-date')

    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense')
    else:
        form = ExpenseForm()

    return render(request, 'expense.html', {
        'form': form,
        'expenses': expenses
    })
# ✅ FINANCIAL DASHBOARD
@login_required(login_url='login')
def financial_dashboard(request):

    user_expenses = Expense.objects.filter(user=request.user)

    # 🔹 Total Expense (All Time)
    total_expense = user_expenses.aggregate(
        Sum('amount')
    )['amount__sum'] or 0

    # 🔹 Total Number of Transactions
    expense_count = user_expenses.count()

    # 🔹 Current Month Expense
    now = timezone.now()

    monthly_expense = user_expenses.filter(
        date__year=now.year,
        date__month=now.month
    ).aggregate(
        Sum('amount')
    )['amount__sum'] or 0

    # 🔹 Recent 5 Transactions
    recent_expenses = user_expenses.order_by('-date')[:5]

    # 🔥 NEW PART — Category-wise Pie Chart Data
    category_data = (
        user_expenses
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by()
    )

    categories = []
    totals = []

    for item in category_data:
        categories.append(item['category'])
        totals.append(float(item['total']))

    context = {
        'total_expense': total_expense,
        'monthly_expense': monthly_expense,
        'expense_count': expense_count,
        'recent_expenses': recent_expenses,
        'categories': categories,   # 👈 for chart
        'totals': totals            # 👈 for chart
    }

    return render(request, 'financial_dashboard.html', context)


# ✅ BUDGET & GOALS VIEW
@login_required(login_url='login')
def budget_goals(request):

    budgets = Budget.objects.filter(user=request.user)
    goals = Goal.objects.filter(user=request.user)

    budget_data = []

    for budget in budgets:
        # Calculate total spent in this category
        spent = Expense.objects.filter(
            user=request.user,
            category=budget.category
        ).aggregate(total=Sum('amount'))['total'] or 0

        # Calculate percentage used
        if budget.monthly_limit > 0:
            percentage = (spent / budget.monthly_limit) * 100
        else:
            percentage = 0

        budget_data.append({
            'category': budget.category,
            'monthly_limit': budget.monthly_limit,
            'spent': spent,
            'percentage': percentage
        })

    context = {
        'budget_data': budget_data,
        'goals': goals
    }

    return render(request, 'budget_goals.html', context)
@login_required(login_url='login')
def create_budget(request):
    if request.method == "POST":
        category = request.POST.get('category')
        monthly_limit = request.POST.get('monthly_limit')

        if Budget.objects.filter(user=request.user, category=category).exists():
            messages.error(request, "⚠️ Budget already exists!")
        else:
            Budget.objects.create(
                user=request.user,
                category=category,
                monthly_limit=monthly_limit
            )
            messages.success(request, "✅ Budget created!")

    return redirect('budget_goals')
@login_required(login_url='login')
def create_goal(request):
    if request.method == "POST":
        title = request.POST.get('title')
        target_amount = request.POST.get('target_amount')
        deadline = request.POST.get('deadline')

        Goal.objects.create(
            user=request.user,
            title=title,
            target_amount=target_amount,
            deadline=deadline
        )

        messages.success(request, "🎯 Goal added successfully!")

    return redirect('budget_goals')


# ✅ LOGOUT
def logout_view(request):
    logout(request)
    return redirect('landing')

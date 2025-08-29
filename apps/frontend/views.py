from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth # Import auth module
from apps.accounts.models import Account
from apps.transaction_history.models import TransactionHistory
from django.db.models import Sum
from .forms import LoginForm, RegisterForm # Import the new forms

# Create your views here.

@login_required # Ensure user is logged in to access dashboard
def dashboard_view(request):
    user_accounts = Account.objects.filter(user=request.user)
    total_balance = user_accounts.aggregate(Sum('balance'))['balance__sum'] or 0

    recent_transactions = TransactionHistory.objects.filter(
        account__user=request.user
    ).order_by('-id')[:5]

    context = {
        'total_balance': total_balance,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'dashboard.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.user_cache # User is stored in form.user_cache by clean method
            auth.login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') # Redirect to login after successful registration
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def accounts_list_view(request):
    return render(request, 'accounts_list.html')

@login_required
def transactions_list_view(request):
    return render(request, 'transactions_list.html')
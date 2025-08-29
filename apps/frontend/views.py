from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.accounts.models import Account
from apps.transaction_history.models import TransactionHistory
from django.db.models import Sum # For calculating total balance

# Create your views here.

@login_required # Ensure user is logged in to access dashboard
def dashboard_view(request):
    user_accounts = Account.objects.filter(user=request.user)
    total_balance = user_accounts.aggregate(Sum('balance'))['balance__sum'] or 0

    # Fetch recent transactions (e.g., last 5)
    recent_transactions = TransactionHistory.objects.filter(
        account__user=request.user
    ).order_by('-id')[:5] # Order by ID descending to get most recent

    context = {
        'total_balance': total_balance,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'dashboard.html', context)

def login_view(request):
    # If user is already authenticated, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'login.html')

def register_view(request):
    # If user is already authenticated, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'register.html')

@login_required
def accounts_list_view(request):
    return render(request, 'accounts_list.html')

@login_required
def transactions_list_view(request):
    return render(request, 'transactions_list.html')
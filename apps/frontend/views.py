from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from apps.accounts.models import Account
from apps.transaction_history.models import TransactionHistory
from django.db.models import Sum
from .forms import LoginForm, RegisterForm, AccountForm # Import AccountForm
from django.contrib import messages # Import messages framework

# Create your views here.

@login_required
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
            user = form.user_cache
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
            messages.success(request, '회원가입이 완료되었습니다. 로그인해주세요.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def accounts_list_view(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            # account_number and initial balance will be set by the model's save method or a signal
            # For now, we'll just save with the user
            form.save(user=request.user)
            messages.success(request, '새 계좌가 성공적으로 추가되었습니다.')
            return redirect('accounts_list') # Redirect to refresh the list
        else:
            # If form is invalid, render the page with errors and keep modal open
            messages.error(request, '계좌 추가에 실패했습니다. 오류를 확인해주세요.')
    else:
        form = AccountForm() # For GET request or invalid POST

    accounts = Account.objects.filter(user=request.user).order_by('id')
    context = {
        'accounts': accounts,
        'form': form, # Pass the form to the template
    }
    return render(request, 'accounts_list.html', context)

@login_required
def transactions_list_view(request):
    transactions = TransactionHistory.objects.filter(account__user=request.user).order_by('-id')
    context = {
        'transactions': transactions
    }
    return render(request, 'transactions_list.html', context)
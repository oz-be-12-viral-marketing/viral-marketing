from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from apps.accounts.models import Account
from apps.transaction_history.models import TransactionHistory
from django.db.models import Sum, F # Import F for database expressions
from django.db.models.functions import ExtractMonth # For extracting month from date
from datetime import datetime, timezone # Import datetime and timezone

# Create your views here.

@login_required
def dashboard_view(request):
    user_accounts = Account.objects.filter(user=request.user)
    total_balance = user_accounts.aggregate(Sum('balance'))['balance__sum'] or 0

    recent_transactions = TransactionHistory.objects.filter(
        account__user=request.user
    ).order_by('-id')[:5]

    # --- Chart Data ---
    # Get current year
    current_year = datetime.now(timezone.utc).year

    # Aggregate monthly income
    monthly_income = TransactionHistory.objects.filter(
        account__user=request.user,
        transaction_type='DEPOSIT',
        created_at__year=current_year
    ).annotate(month=ExtractMonth('created_at')).values('month').annotate(total=Sum('amount')).order_by('month')

    # Aggregate monthly expenses
    monthly_expenses = TransactionHistory.objects.filter(
        account__user=request.user,
        transaction_type='WITHDRAW',
        created_at__year=current_year
    ).annotate(month=ExtractMonth('created_at')).values('month').annotate(total=Sum('amount')).order_by('month')

    # Prepare data for Chart.js
    months = [str(i) for i in range(1, 13)] # Months 1-12
    income_data = [0] * 12
    expense_data = [0] * 12

    for item in monthly_income:
        income_data[item['month'] - 1] = float(item['total'])

    for item in monthly_expenses:
        expense_data[item['month'] - 1] = float(item['total'])
    
    # --- End Chart Data ---

    context = {
        'total_balance': total_balance,
        'recent_transactions': recent_transactions,
        'months': months,
        'income_data': income_data,
        'expense_data': expense_data,
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
            form.save(user=request.user)
            messages.success(request, '새 계좌가 성공적으로 추가되었습니다.')
            return redirect('accounts_list')
        else:
            messages.error(request, '계좌 추가에 실패했습니다. 오류를 확인해주세요.')
    else:
        form = AccountForm() # For GET request or invalid POST

    accounts = Account.objects.filter(user=request.user).order_by('id')
    context = {
        'accounts': accounts,
        'form': form,
    }
    return render(request, 'accounts_list.html', context)

@login_required
def transactions_list_view(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user) # Pass user to form for queryset
        if form.is_valid():
            transaction = form.save(commit=False) # Don't commit yet, need to update balance
            
            # Update account balance
            account = transaction.account
            if transaction.transaction_type == 'DEPOSIT':
                account.balance += transaction.amount
            elif transaction.transaction_type == 'WITHDRAW':
                account.balance -= transaction.amount
            
            account.save() # Save updated account balance
            transaction.balance_after = account.balance # Set balance_after
            transaction.save() # Save transaction

            messages.success(request, '새 거래 내역이 성공적으로 추가되었습니다.')
            return redirect('transactions_list')
        else:
            messages.error(request, '거래 내역 추가에 실패했습니다. 오류를 확인해주세요.')
    else:
        form = TransactionForm(user=request.user) # Pass user to form for queryset

    transactions = TransactionHistory.objects.filter(account__user=request.user).order_by('-id')
    context = {
        'transactions': transactions,
        'form': form,
    }
    return render(request, 'transactions_list.html', context)
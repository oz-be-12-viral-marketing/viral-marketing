from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum, OuterRef, Subquery
from django.db.models.functions import ExtractMonth
from datetime import datetime, timezone

from apps.accounts.models import Account
from apps.transaction_history.models import TransactionHistory
from apps.analysis.models import SentimentAnalysis, SpendingReport # Added SpendingReport
from apps.transaction_history.filters import TransactionFilter
from apps.analysis.filters import AnalysisFilter
from apps.analysis.forms import SentimentAnalysisEditForm
from .forms import AccountForm, TransactionForm, LoginForm


def login_page_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm()
    return render(request, 'login.html', {'form': form})


class MainPageView(TemplateView):
    template_name = "main.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().get(request, *args, **kwargs)


@login_required
def dashboard_view(request):
    user_accounts = Account.objects.filter(user=request.user)
    total_balance = user_accounts.aggregate(Sum('balance'))['balance__sum'] or 0
    recent_transactions = TransactionHistory.objects.filter(account__user=request.user).order_by('-id')[:5]
    current_year = datetime.now(timezone.utc).year
    monthly_income = TransactionHistory.objects.filter(
        account__user=request.user, transaction_type='DEPOSIT', created_at__year=current_year
    ).annotate(month=ExtractMonth('created_at')).values('month').annotate(total=Sum('amount')).order_by('month')
    monthly_expenses = TransactionHistory.objects.filter(
        account__user=request.user, transaction_type='WITHDRAW', created_at__year=current_year
    ).annotate(month=ExtractMonth('created_at')).values('month').annotate(total=Sum('amount')).order_by('month')
    months = [str(i) for i in range(1, 13)]
    income_data = [0] * 12
    expense_data = [0] * 12
    for item in monthly_income:
        income_data[item['month'] - 1] = float(item['total'])
    for item in monthly_expenses:
        expense_data[item['month'] - 1] = float(item['total'])
    context = {
        'total_balance': total_balance,
        'recent_transactions': recent_transactions,
        'months': months,
        'income_data': income_data,
        'expense_data': expense_data,
    }
    return render(request, 'dashboard.html', context)


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
        form = AccountForm()
    accounts = Account.objects.filter(user=request.user).order_by('id')
    context = {
        'accounts': accounts,
        'form': form,
    }
    return render(request, 'accounts_list.html', context)


@login_required
def transactions_list_view(request):
    # Initialize the form for both GET and POST invalid cases
    form = TransactionForm(user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)  # Re-bind form with POST data
        if form.is_valid():
            transaction = form.save(commit=False)
            account = transaction.account
            print(f"DEBUG: Before update - Account ID: {account.id}, Balance: {account.balance}, Transaction Type: {transaction.transaction_type}, Amount: {transaction.amount}") # DEBUG

            if transaction.transaction_type == 'DEPOSIT':
                account.balance += transaction.amount
            elif transaction.transaction_type == 'WITHDRAW':
                account.balance -= transaction.amount
            
            print(f"DEBUG: After update - Account ID: {account.id}, New Balance: {account.balance}") # DEBUG
            account.save()
            transaction.balance_after = account.balance
            transaction.save()
            messages.success(request, '새 거래 내역이 성공적으로 추가되었습니다.')
            return redirect('transactions_list')
        else:
            # If form is invalid, it will fall through and be rendered with errors
            messages.error(request, '거래 내역 추가에 실패했습니다. 양식을 확인해주세요.')

    # --- This part runs for GET requests or after an invalid POST ---
    sentiment_analysis_subquery = SentimentAnalysis.objects.filter(
        transaction=OuterRef('pk')
    ).values('pk')[:1]
    transaction_list = TransactionHistory.objects.filter(account__user=request.user).annotate(
        analysis_id=Subquery(sentiment_analysis_subquery)
    ).order_by('-created_at')
    transaction_filter = TransactionFilter(request.GET, queryset=transaction_list)

    paginator = Paginator(transaction_filter.qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': transaction_filter,
        'page_obj': page_obj,
        'form': form,  # This will be either a blank form or the invalid form with errors
    }
    return render(request, 'transactions_list.html', context)


@login_required
def profile_view(request):
    return render(request, 'profile.html')

def logged_out_view(request):
    return render(request, 'logged_out.html')


@login_required
def signup_complete_view(request):
    return render(request, 'account/signup_complete.html')


@login_required
def transaction_analysis_form_view(request, transaction_id):
    transaction = get_object_or_404(TransactionHistory, pk=transaction_id, account__user=request.user)
    context = {
        'transaction': transaction
    }
    return render(request, 'frontend/transaction_analysis_form.html', context)


@login_required
def analysis_history_view(request):
    analysis_list = SentimentAnalysis.objects.filter(transaction__account__user=request.user).order_by('-transaction__created_at')
    analysis_filter = AnalysisFilter(request.GET, queryset=analysis_list)

    paginator = Paginator(analysis_filter.qs, 9)  # Show 9 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'filter': analysis_filter,
        'page_obj': page_obj,
    }
    return render(request, 'frontend/analysis_history.html', context)


@login_required
def transaction_delete_view(request, transaction_id):
    transaction = get_object_or_404(TransactionHistory, pk=transaction_id, account__user=request.user)
    if request.method == 'POST':
        account = transaction.account
        # Adjust account balance before deleting transaction
        if transaction.transaction_type == 'DEPOSIT':
            account.balance -= transaction.amount
        elif transaction.transaction_type == 'WITHDRAW':
            account.balance += transaction.amount
        account.save()
        transaction.delete()
        messages.success(request, '거래 내역이 성공적으로 삭제되었습니다.')
        return redirect('transactions_list')
    # If not a POST request, just redirect to the list
    return redirect('transactions_list')


@login_required
def analysis_edit_view(request, analysis_id):
    analysis = get_object_or_404(SentimentAnalysis, pk=analysis_id, transaction__account__user=request.user)

    # Ensure sentiment value matches form choices
    if analysis.sentiment == 'POSITIVE' or analysis.sentiment == 'LABEL_0':
        analysis.sentiment = '긍정'
    elif analysis.sentiment == 'NEGATIVE' or analysis.sentiment == 'LABEL_1':
        analysis.sentiment = '부정'

    if request.method == 'POST':
        form = SentimentAnalysisEditForm(request.POST, instance=analysis)
        if form.is_valid():
            form.save()
            messages.success(request, '분석 내역이 성공적으로 수정되었습니다.')
            return redirect('analysis_history')
    else:
        form = SentimentAnalysisEditForm(instance=analysis)
    
    context = {
        'form': form,
        'analysis': analysis
    }
    return render(request, 'frontend/analysis_edit_form.html', context)


@login_required
def generate_reports_view(request):
    # 최신 주간 리포트 JSON 데이터 가져오기 (현재 사용자 기준)
    weekly_report = SpendingReport.objects.filter(
        user=request.user, # Filter by current user
        report_type='weekly'
    ).order_by('-generated_date', '-created_at').first()
    weekly_report_json_data = weekly_report.json_data if weekly_report else '{}' # Default to empty JSON string

    # 최신 월간 리포트 JSON 데이터 가져오기 (현재 사용자 기준)
    monthly_report = SpendingReport.objects.filter(
        user=request.user, # Filter by current user
        report_type='monthly'
    ).order_by('-generated_date', '-created_at').first()
    monthly_report_json_data = monthly_report.json_data if monthly_report else '{}' # Default to empty JSON string

    context = {
        'weekly_report_json_data': weekly_report_json_data,
        'monthly_report_json_data': monthly_report_json_data,
    }
    return render(request, 'frontend/spending_reports.html', context)
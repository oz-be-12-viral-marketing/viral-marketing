from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

def dashboard_view(request):
    return render(request, 'dashboard.html')

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')

@login_required
def accounts_list_view(request):
    return render(request, 'accounts_list.html')

@login_required
def transactions_list_view(request):
    return render(request, 'transactions_list.html')
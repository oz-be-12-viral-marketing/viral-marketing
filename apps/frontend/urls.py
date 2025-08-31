from django.urls import path
from . import views
from .views import MainPageView


urlpatterns = [
    path('', MainPageView.as_view(), name='main'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('login/', views.login_page_view, name='login'),
    path('accounts/', views.accounts_list_view, name='accounts_list'),
    path('transactions/', views.transactions_list_view, name='transactions_list'),
    path('profile/', views.profile_view, name='profile'),
    path('logged-out/', views.logged_out_view, name='logged_out'),
    path('accounts/signup/complete/', views.signup_complete_view, name='account_signup_complete'),
    path('transactions/<int:transaction_id>/analyze/', views.transaction_analysis_form_view, name='transaction_analysis_form'),
    path('analysis-history/', views.analysis_history_view, name='analysis_history'),
]

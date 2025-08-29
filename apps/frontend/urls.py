from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('accounts/', views.accounts_list_view, name='accounts_list'),
    path('transactions/', views.transactions_list_view, name='transactions_list'),
    path('profile/', views.profile_view, name='profile'),
    path('logged-out/', views.logged_out_view, name='logged_out'),
]
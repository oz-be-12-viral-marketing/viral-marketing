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
]

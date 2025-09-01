from django.urls import path
from . import views

urlpatterns = [
    path('generate-report/<str:period_type>/', views.generate_report_api_view, name='generate_report_api'),
    path('transactions/<int:transaction_id>/sentiment/', views.sentiment_analysis_api_view, name='sentiment_analysis_api'),
    path('reports/', views.report_list_api_view, name='report_list_api'),
]
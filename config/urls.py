"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from apps.users.views import EmailVerificationView, LoginView, LogoutView, RegisterView, UserDetailView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("accounts/", include("allauth.urls")),
    path("activate/<uidb64>/<token>/", EmailVerificationView.as_view(), name="activate-user"),
    path("users/register/", RegisterView.as_view()),
    path("users/login/", LoginView.as_view()),
    path("users/logout/", LogoutView.as_view()),
    path("users/detail/", UserDetailView.as_view(), name="user-detail"),
    path("api/v1/", include("apps.accounts.urls")),
    path("api/v1/", include("apps.transaction_history.urls")),
    path("api/analysis/", include("apps.analysis.urls")),
]

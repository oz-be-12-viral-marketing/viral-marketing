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

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from apps.users.views import EmailVerificationView, LoginView, UserDetailView, TokenRefreshView

urlpatterns = [
    path("api/v1/users/login/", LoginView.as_view(), name="api_login"),
    path("", include("apps.frontend.urls")),
    path("admin/", admin.site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("accounts/", include("allauth.urls")),
    path("activate/<uidb64>/<token>/", EmailVerificationView.as_view(), name="activate-user"),
    path("users/logout/", DjangoLogoutView.as_view(next_page='logged_out'), name="logout"),
    path("api/v1/users/me/", UserDetailView.as_view(), name="user-detail"),
    path("users/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"), # Added
    path("api/v1/", include("apps.accounts.urls")),
    path("api/v1/", include("apps.transaction_history.urls")),
    path("api/v1/analysis/", include("apps.analysis.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

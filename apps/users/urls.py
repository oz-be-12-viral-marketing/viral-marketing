from django.urls import path

from apps.users.views import EmailVerificationView, LoginView, LogoutView, RegisterView, UserDetailView

urlpatterns = [
    path("activate/<uidb64>/<token>/", EmailVerificationView.as_view(), name="activate-user"),
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view()),
    path("detail/", UserDetailView.as_view(), name="user-detail"),
]

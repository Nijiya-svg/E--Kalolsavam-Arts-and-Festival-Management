from django.urls import path

from .views import UserLoginView, UserLogoutView, UserSignupView, dashboard_redirect

app_name = "accounts"

urlpatterns = [
    path("", UserLoginView.as_view(), name="login"),
    path("signup/", UserSignupView.as_view(), name="signup"),
    path("dashboard/", dashboard_redirect, name="dashboard"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import EmailAuthenticationForm, SignUpForm
from .models import User


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("accounts:dashboard")


class UserSignupView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:dashboard")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Account created successfully.")
        return response


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")


@login_required
def dashboard_redirect(request):
    role = request.user.role
    if request.user.is_superuser or role == User.ROLE_ADMIN:
        return redirect("/admin/")
    if role == User.ROLE_STUDENT:
        return redirect("events:student-events")
    if role == User.ROLE_JUDGE:
        return redirect("judges:judge-events")
    if role == User.ROLE_VOLUNTEER:
        return redirect("volunteers:volunteer-duty")

    messages.error(request, "Your account role is not configured.")
    return redirect("accounts:login")

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Student


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        existing_user = Student.objects.filter(email__iexact=email).first()
        if existing_user and not existing_user.has_usable_password():
            messages.error(
                request,
                "Your account password was not set correctly. Please sign up again with the same email to reset it.",
            )
            return redirect("signup")
        messages.error(request, "Invalid email or password")

    return render(request, "student/login.html")


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        name = request.POST.get("name")
        school = request.POST.get("school")
        course = request.POST.get("course")
        gender = request.POST.get("gender")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password = request.POST.get("password") or request.POST.get("password1")
        confirm = request.POST.get("confirm_password") or request.POST.get("password2")

        if not all([name, school, course, gender, phone, email, password, confirm]):
            messages.error(request, "Please fill all fields")
            return render(request, "student/signup.html")

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return render(request, "student/signup.html")

        existing_user = Student.objects.filter(email__iexact=email).first()
        if existing_user and existing_user.has_usable_password():
            messages.error(request, "Email already registered")
            return render(request, "student/signup.html")
        if existing_user and not existing_user.has_usable_password():
            existing_user.name = name
            existing_user.school = school
            existing_user.course = course
            existing_user.gender = gender
            existing_user.phone = phone
            existing_user.email = email
            existing_user.set_password(password)
            existing_user.is_active = True
            existing_user.save()
            recovered_user = authenticate(request, username=email, password=password)
            if recovered_user is not None:
                login(request, recovered_user)
                return redirect("home")
            messages.error(request, "Account recovered, please login again.")
            return redirect("login")

        user = Student.objects.create_user(
            email=email,
            password=password,
            name=name,
            school=school,
            course=course,
            gender=gender,
            phone=phone,
        )
        authenticated_user = authenticate(request, username=email, password=password)
        if authenticated_user is not None:
            login(request, authenticated_user)
            return redirect("home")
        messages.success(request, "Account created. Please login.")
        return redirect("login")

    return render(request, "student/signup.html")


@login_required
def home(request):
    return render(request, "student/home.html")


@login_required
def register_for_events(request):
    return render(request, "student/register.html")


@login_required
def my_participations(request):
    return render(request, "student/my_participation.html")


def logout_view(request):
    logout(request)
    return redirect("login")

# frontend/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken


def home_view(request):
    return render(request, "home.html")


def admin_view(request):
    return redirect("/admin")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect("frontend:home")  # Use namespace
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password
                )
                user.save()
                login(request, user)
                messages.success(request, "Registration successful!")
                return redirect("frontend:home")  # Use namespace
        else:
            messages.error(request, "Passwords do not match.")
    return render(request, "register.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("frontend:home")  # Use namespace


def token_generator_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return render(
                request,
                "token_generator.html",
                {
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                },
            )
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, "token_generator.html")

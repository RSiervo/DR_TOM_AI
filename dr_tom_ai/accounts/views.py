from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django import forms

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta(UserCreationForm.Meta):
        fields = ("username", "email")

def login_view(request):
    if request.user.is_authenticated:
        return redirect('analyze')
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Welcome back!")
            return redirect('analyze')
        messages.error(request, "Invalid credentials.")
    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    messages.info(request, "You’ve been logged out.")
    return redirect('home')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('analyze')
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created. Welcome!")
            return redirect('analyze')
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})
